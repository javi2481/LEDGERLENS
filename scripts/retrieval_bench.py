#!/usr/bin/env python3
"""Keyword vs vector vs hybrid retrieval bench. Skip without RAGFlow. Not identity gold."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.ragflow_http import (
    SKIP_NO_RAGFLOW,
    api,
    chunk_to_hit,
    load_env,
    ragflow_reachable,
    resolve_api_token,
    rows_of,
)
from schemas.retrieval_metrics import score_case, summarize_arm

GOLD = ROOT / "evals" / "retrieval_v1.json"
OUT = ROOT / "outputs" / "retrieval_run.json"
ARMS = (("keyword", 0.0), ("vector", 1.0), ("hybrid", 0.3))


def _dataset_id(token: str, wanted: str) -> str | None:
    rows = rows_of(api("GET", "/datasets?page_size=100", token), "datasets", "kbs")
    for row in rows:
        if (row.get("name") or "") == wanted:
            return str(row["id"])
    if len(rows) == 1:
        return str(rows[0]["id"])
    return None


def retrieve(token: str, dataset_id: str, question: str, weight: float, top_k: int, threshold: float) -> list[dict]:
    payload = {
        "question": question,
        "dataset_ids": [dataset_id],
        "similarity_threshold": threshold,
        "vector_similarity_weight": weight,
        "top_k": top_k,
        "rerank_id": "",
    }
    body = api("POST", "/retrieval", token, json.dumps(payload).encode())
    chunks = rows_of(body, "chunks")
    hits: list[dict] = []
    for chunk in chunks:
        hit = chunk_to_hit(chunk)
        if hit is not None:
            hits.append(hit)
    return hits[:top_k]


def main() -> int:
    load_env()
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    if not ragflow_reachable():
        report = {"skipped": True, "reason": SKIP_NO_RAGFLOW, "arms": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    token = resolve_api_token()
    if not token:
        report = {"skipped": True, "reason": SKIP_NO_RAGFLOW, "arms": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    dataset = gold.get("dataset") or "demo_4"
    ds_id = _dataset_id(token, dataset)
    if not ds_id:
        report = {"skipped": True, "reason": "no_dataset", "arms": {}, "cases": []}
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return 0
    top_k = int(gold.get("top_k") or 10)
    threshold = float(gold.get("similarity_threshold") or 0.3)
    case_rows: list[dict] = []
    arm_scores: dict[str, list[dict]] = {name: [] for name, _w in ARMS}
    for case in gold["cases"]:
        rankings: dict[str, list] = {}
        for name, weight in ARMS:
            hits = retrieve(token, ds_id, case["question"], weight, top_k, threshold)
            rankings[name] = hits
            arm_scores[name].append(score_case(hits, case["relevant"]))
        case_rows.append({"id": case["id"], "rankings": rankings})
    summary = {name: summarize_arm(arm_scores[name]) for name, _w in ARMS}
    report = {
        "skipped": False,
        "reason": None,
        "dataset": dataset,
        "top_k": top_k,
        "summary": summary,
        "cases": case_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
