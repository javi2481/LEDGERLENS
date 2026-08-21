"""Gold files for the RAG pilot: 20 qrels, 10 chat cases. Offline."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "docs" / "archivos_muestra"


def test_retrieval_v1_has_twenty_page_qrels() -> None:
    payload = json.loads((ROOT / "evals" / "retrieval_v1.json").read_text(encoding="utf-8"))
    cases = payload["cases"]
    assert len(cases) == 20
    names = {p.name for p in SAMPLES.glob("*.pdf")}
    for case in cases:
        assert "identity_key" not in case
        assert case["relevant"]
        for hit in case["relevant"]:
            assert hit["doc"] in names
            assert isinstance(hit["page"], int) and hit["page"] >= 1
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))


def test_rag_chat_v1_partitions() -> None:
    payload = json.loads((ROOT / "evals" / "rag_chat_v1.json").read_text(encoding="utf-8"))
    cases = payload["cases"]
    assert len(cases) == 10
    by = {}
    for case in cases:
        by[case["partition"]] = by.get(case["partition"], 0) + 1
    assert by["identity"] == 4
    assert by["narrative"] == 3
    assert by["abstention"] == 2
    assert by["comparison"] == 1
    neto = next(c for c in cases if c["id"] == "ch-id-01")
    assert neto["expected_value"] == "21262335"
    ltm = next(c for c in cases if c["id"] == "ch-id-03")
    assert ltm["expected_value"] == "76"


def test_identity_harness_does_not_import_ragflow() -> None:
    for name in ("lookup.py", "extract.py", "store.py", "classify.py"):
        text = (ROOT / "schemas" / name).read_text(encoding="utf-8")
        assert "ragflow" not in text.lower()
        assert "urllib" not in text.lower()
