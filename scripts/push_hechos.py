#!/usr/bin/env python3
"""Inject Graph EEFF identity into every chat and every EEFF that needs it.

Scans all RAGFlow datasets for dedicated EEFF PDFs, attaches a manual Graph
chunk to each matched filing (Show Quote cites the PDF), and upserts Graph
rules + fichas into every chat assistant. Does not reparse MinerU. Not called
by scripts/up.sh.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph_hechos import (  # noqa: E402
    MARKER,
    SIDECAR,
    ficha_chunk,
    fichas_prompt_lines,
    load_catalog,
    load_output_fichas,
    merge_fichas,
    needs_graph,
    upsert_graph_prompt,
)

API = os.environ.get("RAGFLOW_URL", "http://127.0.0.1/api/v1").rstrip("/")


def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def token_from_mysql() -> str:
    cmd = (
        'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N rag_flow '
        '-e "SELECT token FROM api_token LIMIT 1;"'
    )
    out = subprocess.check_output(
        ["docker", "exec", "ledgerlens-mysql-1", "sh", "-c", cmd],
        stderr=subprocess.DEVNULL,
    )
    token = out.decode("utf-8", errors="replace").strip().splitlines()[-1].strip()
    if not token:
        raise SystemExit("error: no api_token in rag_flow")
    return token


def api(method: str, path: str, token: str, data: bytes | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}"},
    )
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"error: {method} {path} -> {exc.code} {body[:500]}") from exc


def rows_of(payload: dict, *keys: str) -> list:
    data = payload.get("data") or []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            if isinstance(data.get(key), list):
                return data[key]
    return []


def list_chunks(ds_id: str, doc_id: str, token: str) -> list:
    chunks: list = []
    page = 1
    while page <= 20:
        body = api(
            "GET",
            f"/datasets/{ds_id}/documents/{doc_id}/chunks?page={page}&page_size=100",
            token,
        )
        batch = rows_of(body, "chunks")
        chunks.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return chunks


def delete_graph_chunks(ds_id: str, doc_id: str, token: str) -> int:
    ids = []
    for chunk in list_chunks(ds_id, doc_id, token):
        text = chunk.get("content") or chunk.get("content_with_weight") or ""
        if MARKER in text:
            cid = chunk.get("id") or chunk.get("chunk_id")
            if cid:
                ids.append(cid)
    if not ids:
        return 0
    api(
        "DELETE",
        f"/datasets/{ds_id}/documents/{doc_id}/chunks",
        token,
        json.dumps({"chunk_ids": ids}).encode(),
    )
    return len(ids)


def add_graph_chunk(
    ds_id: str,
    doc_id: str,
    token: str,
    content: str,
    keywords: list[str],
    questions: list[str],
) -> None:
    added = api(
        "POST",
        f"/datasets/{ds_id}/documents/{doc_id}/chunks",
        token,
        json.dumps(
            {
                "content": content,
                "important_keywords": keywords,
                "questions": questions,
            }
        ).encode(),
    )
    if added.get("code") not in (0, None):
        raise SystemExit(f"error: add chunk {added}")


def chat_dataset_ids(chat: dict) -> list[str]:
    raw = chat.get("dataset_ids") or chat.get("kb_ids") or []
    if isinstance(raw, str):
        return [raw]
    return [str(x) for x in raw]


def main() -> int:
    load_env(ROOT / ".env")
    token = os.environ.get("RAGFLOW_API_KEY") or token_from_mysql()
    fichas = merge_fichas(load_catalog(), load_output_fichas())
    by_name = {row["name"]: row for row in fichas}
    if not fichas:
        print("error: no Graph fichas in docs/hechos_eeff.json or outputs/*/ficha.json", file=sys.stderr)
        return 1

    datasets = rows_of(api("GET", "/datasets?page_size=100", token), "datasets", "kbs")
    if not datasets:
        print("error: no datasets via API", file=sys.stderr)
        return 1

    attached_by_dataset: dict[str, list[dict]] = {}
    for ds in datasets:
        ds_id = ds["id"]
        ds_name = ds.get("name") or ds_id
        docs = rows_of(
            api("GET", f"/datasets/{ds_id}/documents?page_size=100", token),
            "docs",
            "documents",
        )
        print(f"ok: dataset {ds_name} ({len(docs)} docs)")
        sidecar = next((d for d in docs if d.get("name") == SIDECAR), None)
        if sidecar:
            api(
                "DELETE",
                f"/datasets/{ds_id}/documents",
                token,
                json.dumps({"ids": [sidecar["id"]]}).encode(),
            )
            print(f"ok: {ds_name}: removed {SIDECAR}")

        compare_labels = [
            by_name[d["name"]].get("label") or d["name"]
            for d in docs
            if d.get("name") in by_name
        ]
        attached: list[dict] = []
        for doc in docs:
            name = doc.get("name") or ""
            if name not in by_name:
                if needs_graph(name):
                    print(
                        f"skip: {ds_name}/{name} needs Graph but has no ficha "
                        f"(run: python scripts/run_docling_graph_eeff.py --pdf ...)",
                        file=sys.stderr,
                    )
                continue
            row = by_name[name]
            removed = delete_graph_chunks(ds_id, doc["id"], token)
            content, keywords, questions = ficha_chunk(row, compare_labels)
            add_graph_chunk(ds_id, doc["id"], token, content, keywords, questions)
            attached.append(row)
            extra = f" (replaced {removed})" if removed else ""
            print(f"ok: {ds_name}/{name} Graph chunk{extra}")
        attached_by_dataset[ds_id] = attached

    chats = rows_of(api("GET", "/chats?page_size=100", token), "chats")
    if not chats:
        print("error: no chats via API", file=sys.stderr)
        return 1

    for chat in chats:
        ds_ids = chat_dataset_ids(chat)
        rows = []
        seen: set[str] = set()
        for ds_id in ds_ids or attached_by_dataset:
            for row in attached_by_dataset.get(ds_id, []):
                key = row["name"]
                if key not in seen:
                    seen.add(key)
                    rows.append(row)
        if not rows:
            rows = fichas
        prompt = dict(chat.get("prompt_config") or {})
        prompt["system"] = upsert_graph_prompt(prompt.get("system") or "", fichas_prompt_lines(rows))
        prompt["quote"] = True
        api(
            "PUT",
            f"/chats/{chat['id']}",
            token,
            json.dumps({"prompt_config": prompt}).encode(),
        )
        print(f"ok: chat {chat.get('name')} ({len(rows)} fichas, quote on)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
