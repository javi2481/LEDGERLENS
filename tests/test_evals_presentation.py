"""Presentation evals: exact-match EBITDA/LTM. Finance and press remain regression."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from schemas.corpus import extract_claims_from_dir
from schemas.lookup import lookup
from schemas.parse_artifact import fixtures_ready

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "presentation_v1.json"

needs_parse = pytest.mark.skipif(
    not fixtures_ready(),
    reason="missing MinerU fixtures (run scripts/export_mineru.py)",
)


def _load_cases() -> list[dict]:
    payload = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    return list(payload["cases"])


@pytest.fixture(scope="module")
def claims():
    if not fixtures_ready():
        pytest.skip("missing MinerU fixtures (run scripts/export_mineru.py)")
    return extract_claims_from_dir()


@needs_parse
def test_presentation_identity(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "identity":
            continue
        result = lookup(case["question"], claims)
        if result.route != "identity" or len(result.claims) != 1:
            failures.append(f"{case['id']} route={result.route} n={len(result.claims)}")
            continue
        row = result.claims[0]
        if row.identity_key != case["expected_identity"]:
            failures.append(f"{case['id']} identity {row.identity_key}")
        if row.value != case["expected_value"]:
            failures.append(f"{case['id']} value {row.value}")
        if row.period != case["expected_period"]:
            failures.append(f"{case['id']} period {row.period}")
        if row.source_page != case["expected_source_page"]:
            failures.append(f"{case['id']} page {row.source_page}")
        prov = case.get("expected_provenance") or ""
        if prov and prov.casefold() not in (row.source_text or "").casefold():
            failures.append(f"{case['id']} provenance missing {prov!r}")
    assert not failures, "\n".join(failures)


@needs_parse
def test_presentation_abstention(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "abstention":
            continue
        result = lookup(case["question"], claims)
        if result.route != "abstain" or result.claims:
            failures.append(f"{case['id']} route={result.route} claims={len(result.claims)}")
    assert not failures, "\n".join(failures)
