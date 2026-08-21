#!/usr/bin/env python3
"""Inject kernel claims into RAGFlow EEFF chunks and chat prompts.

Does not reparse MinerU. Not called by scripts/up.sh. After merge, run once on
the UI host and open a new chat.
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
sys.path.insert(0, str(ROOT))

from schemas.classify import dedicated_financial_statement  # noqa: E402
from schemas.corpus import SAMPLES  # noqa: E402
from schemas.extract import extract_financial_statement  # noqa: E402
from schemas.inject import (  # noqa: E402
    SIDECAR_NAMES,
    eeff_chunk,
    is_inject_chunk,
    prompt_lines,
    upsert_idp_prompt,
)
from schemas.store import load_claims  # noqa: E402

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


def period_for_eeff(name: str) -> str | None:
    pdf = SAMPLES / name
    if not pdf.is_file():
        return None
    row = extract_financial_statement(pdf)
    return row.period if row is not None else None


def attach_plan(docs: list[dict], claims: tuple) -> list[tuple[dict, str, list[str], list[str]]]:
    planned: list[tuple[dict, str, list[str], list[str]]] = []
    for doc in docs:
        name = doc.get("name") or ""
        if name in SIDECAR_NAMES:
            continue
        if not dedicated_financial_statement(name):
            continue
        period = period_for_eeff(name)
        if period is None:
            continue
        built = eeff_chunk(claims, period)
        if built is None:
            continue
        content, keywords, questions = built
        planned.append((doc, content, keywords, questions))
    return planned


def _run_inject(token: str, claims: tuple, api_fn) -> int:
    datasets = rows_of(api_fn("GET", "/datasets?page_size=100", token), "datasets", "kbs")
    if not datasets:
        print("error: no datasets via API", file=sys.stderr)
        return 1

    for ds in datasets:
        ds_id = ds["id"]
        ds_name = ds.get("name") or ds_id
        docs = rows_of(
            api_fn("GET", f"/datasets/{ds_id}/documents?page_size=100", token),
            "docs",
            "documents",
        )
        print(f"ok: dataset {ds_name} ({len(docs)} docs)")
        for doc in docs:
            name = doc.get("name") or ""
            if name in SIDECAR_NAMES:
                api_fn(
                    "DELETE",
                    f"/datasets/{ds_id}/documents",
                    token,
                    json.dumps({"ids": [doc["id"]]}).encode(),
                )
                print(f"ok: {ds_name}: removed {name}")

        planned = attach_plan(docs, claims)
        for doc, content, keywords, questions in planned:
            name = doc.get("name") or ""
            chunks: list = []
            page = 1
            while page <= 20:
                body = api_fn(
                    "GET",
                    f"/datasets/{ds_id}/documents/{doc['id']}/chunks?page={page}&page_size=100",
                    token,
                )
                batch = rows_of(body, "chunks")
                chunks.extend(batch)
                if len(batch) < 100:
                    break
                page += 1
            ids = []
            for chunk in chunks:
                text = chunk.get("content") or chunk.get("content_with_weight") or ""
                if is_inject_chunk(text):
                    cid = chunk.get("id") or chunk.get("chunk_id")
                    if cid:
                        ids.append(cid)
            removed = 0
            if ids:
                api_fn(
                    "DELETE",
                    f"/datasets/{ds_id}/documents/{doc['id']}/chunks",
                    token,
                    json.dumps({"chunk_ids": ids}).encode(),
                )
                removed = len(ids)
            api_fn(
                "POST",
                f"/datasets/{ds_id}/documents/{doc['id']}/chunks",
                token,
                json.dumps(
                    {
                        "content": content,
                        "important_keywords": keywords,
                        "questions": questions,
                    }
                ).encode(),
            )
            extra = f" (replaced {removed})" if removed else ""
            print(f"ok: {ds_name}/{name} IDP chunk{extra}")

    chats = rows_of(api_fn("GET", "/chats?page_size=100", token), "chats")
    if not chats:
        print("error: no chats via API", file=sys.stderr)
        return 1

    block = prompt_lines(claims)
    for chat in chats:
        prompt = dict(chat.get("prompt_config") or {})
        prompt["system"] = upsert_idp_prompt(prompt.get("system") or "", block)
        prompt["quote"] = True
        api_fn(
            "PUT",
            f"/chats/{chat['id']}",
            token,
            json.dumps({"prompt_config": prompt}).encode(),
        )
        print(f"ok: chat {chat.get('name')} (quote on)")
    return 0


def main() -> int:
    load_env(ROOT / ".env")
    token = os.environ.get("RAGFLOW_API_KEY") or token_from_mysql()
    claims, _hit = load_claims()
    if not claims:
        print("error: no kernel claims to inject", file=sys.stderr)
        return 1
    return _run_inject(token, claims, api)


if __name__ == "__main__":
    raise SystemExit(main())
