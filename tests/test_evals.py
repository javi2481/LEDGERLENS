"""Identity evals v1: exact-match by dimension. Narrative cases are skipped."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from schemas.catalog import load_recipes
from schemas.corpus import extract_claims_from_dir
from schemas.lookup import lookup
from schemas.parse_artifact import fixtures_ready

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "identity_v1.json"

needs_parse = pytest.mark.skipif(
    not fixtures_ready(),
    reason="missing MinerU fixtures (run scripts/export_mineru.py)",
)


def _load_cases() -> list[dict]:
    payload = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    return list(payload["cases"])


def _identity_matches(expected: str, actual: str) -> bool:
    exp_parts = expected.split("|")
    act_parts = actual.split("|")
    if len(exp_parts) != len(act_parts):
        return False
    return all(e == "*" or e == a for e, a in zip(exp_parts, act_parts))


def test_eval_file_partitions() -> None:
    cases = _load_cases()
    by_part: dict[str, int] = {}
    for case in cases:
        by_part[case["partition"]] = by_part.get(case["partition"], 0) + 1
    assert by_part["identity"] == 10
    assert by_part["neighbor"] == 10
    assert by_part["comparison"] == 10
    assert by_part["abstention"] == 5
    assert by_part["narrative"] == 10
    narrative = [c for c in cases if c["route"] == "narrative"]
    assert len(narrative) == 10
    assert all(c.get("skip") is True for c in narrative)


def test_eval_numeric_gold_matches_recipe() -> None:
    gold = load_recipes()["financial_statement"].gold
    allowed = {
        gold["BYMA_-_EEFF_31-03-2026_VF.pdf"]["net_income_consolidated"],
        gold["BYMA_-_EEFF_31-03-2026_VF.pdf"]["net_income_attributable_to_parent"],
        gold["BYMA - EEFF 30-06-2026.pdf"]["net_income_consolidated"],
        gold["BYMA - EEFF 30-06-2026.pdf"]["net_income_attributable_to_parent"],
    }
    for case in _load_cases():
        if case["route"] in {"abstain", "narrative"}:
            continue
        if case.get("expected_value"):
            assert case["expected_value"] in allowed
        for value in case.get("expected_values") or ():
            assert value in allowed


@pytest.fixture(scope="module")
def claims():
    if not fixtures_ready():
        pytest.skip("missing MinerU fixtures (run scripts/export_mineru.py)")
    return extract_claims_from_dir()


@needs_parse
def test_identity_value_evidence_period(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["route"] == "narrative" or case.get("skip"):
            continue
        if case["partition"] not in {"identity", "neighbor"}:
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
        for rejected in case.get("reject_values") or ():
            if row.value == rejected:
                failures.append(f"{case['id']} accepted neighbor {rejected}")
    assert not failures, "\n".join(failures)


@needs_parse
def test_comparison_integrity(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "comparison":
            continue
        result = lookup(case["question"], claims)
        if result.route != "identity" or not result.compare or len(result.claims) < 2:
            failures.append(f"{case['id']} compare route={result.route} n={len(result.claims)}")
            continue
        scopes = {c.scope for c in result.claims}
        if len(scopes) != 1:
            failures.append(f"{case['id']} mixed scopes {scopes}")
        for row in result.claims:
            if not _identity_matches(case["expected_identity"], row.identity_key):
                failures.append(f"{case['id']} identity {row.identity_key}")
            if row.source_page != case["expected_source_page"]:
                failures.append(f"{case['id']} page {row.source_page}")
        values = {c.value for c in result.claims}
        if values != set(case["expected_values"]):
            failures.append(f"{case['id']} values {values}")
        periods = {c.period for c in result.claims}
        if periods != set(case["expected_periods"]):
            failures.append(f"{case['id']} periods {periods}")
    assert not failures, "\n".join(failures)


@needs_parse
def test_abstention(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "abstention":
            continue
        result = lookup(case["question"], claims)
        if result.route != "abstain" or result.claims:
            failures.append(f"{case['id']} route={result.route} claims={len(result.claims)}")
        if case.get("expected_abstain") is not True:
            failures.append(f"{case['id']} gold missing expected_abstain")
    assert not failures, "\n".join(failures)


def test_narrative_skipped_not_scored() -> None:
    skipped = 0
    for case in _load_cases():
        if case["route"] == "narrative" or case.get("skip"):
            skipped += 1
            continue
    assert skipped == 10


def test_harness_does_not_contact_ragflow() -> None:
    paths = [
        ROOT / "schemas" / "lookup.py",
        ROOT / "schemas" / "extract.py",
        ROOT / "schemas" / "corpus.py",
        ROOT / "scripts" / "idp_ask.py",
    ]
    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        assert "import ragflow" not in source
        assert "from ragflow" not in source
        assert "import requests" not in source
        assert "import httpx" not in source
        assert "urllib.request" not in source

