#!/usr/bin/env python3
"""Ten-question RAG chat pilot. Skip without RAGFlow. Not identity pytest."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.rag_chat_score import score_chat_case, summarize_chat
from schemas.ragflow_http import SKIP_NO_RAGFLOW, api, load_env, ragflow_reachable, rows_of

GOLD = ROOT / "evals" / "rag_chat_v1.json"
OUT = ROOT / "outputs" / "rag_chat_run.json"


def _token() -> str | None:
    return os.environ.get("RAGFLOW_API_KEY") or None


def _chat_id(token: str, wanted: str) -> str | None:
    rows = rows_of(api("GET", "/chats?page_size=100", token), "chats")
    for row in rows:
        if (row.get("name") or "") == wanted:
            return str(row["id"])
    if len(rows) == 1:
        return str(rows[0]["id"])
    return None


def _cited_from(payload: dict) -> list[str]:
    data = payload.get("data")
    if not isinstance(data, dict):
        return []
    names: list[str] = []
    ref = data.get("reference") or {}
    if isinstance(ref, dict):
        for row in ref.get("doc_aggs") or ref.get("chunks") or []:
            if not isinstance(row, dict):
                continue
            name = row.get("doc_name") or row.get("document_keyword") or row.get("docnm_kwd")
            if name:
                names.append(str(name))
    return names


def _answer_from(payload: dict) -> str:
    data = payload.get("data")
    if isinstance(data, dict):
        return str(data.get("answer") or data.get("content") or "")
    if isinstance(data, str):
        return data
    return str(payload.get("answer") or "")


def ask(token: str, chat_id: str, question: str) -> dict:
    body = api(
        "POST",
        f"/chats/{chat_id}/completions",
        token,
        json.dumps({"question": question, "stream": False}).encode(),
        timeout=120.0,
    )
    answer = _answer_from(body)
    cited = _cited_from(body)
    abstained = "no hay evidencia" in answer.casefold()
    return {"answer": answer, "cited_docs": cited, "abstained": abstained}


def main() -> int:
    load_env()
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    if not ragflow_reachable():
        report = {"skipped": True, "reason": SKIP_NO_RAGFLOW, "summary": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    token = _token()
    if not token:
        report = {"skipped": True, "reason": SKIP_NO_RAGFLOW, "summary": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    wanted = gold.get("assistant") or "chat_demo_4"
    chat_id = _chat_id(token, wanted)
    if not chat_id:
        report = {"skipped": True, "reason": "no_chat", "summary": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    runs: list[dict] = []
    scores: list[dict] = []
    for case in gold["cases"]:
        run = ask(token, chat_id, case["question"])
        run["id"] = case["id"]
        runs.append(run)
        scores.append(score_chat_case(case, run))
    report = {
        "skipped": False,
        "reason": None,
        "assistant": wanted,
        "summary": summarize_chat(scores),
        "cases": runs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
