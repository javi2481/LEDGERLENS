"""Identity evals v2: P&L neighbor rows. v1 remains the neto/controlante regression."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from schemas.catalog import load_recipes
from schemas.corpus import extract_claims_from_dir
from schemas.lookup import lookup

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "identity_v2.json"

needs_pdftotext = pytest.mark.skipif(
    shutil.which("pdftotext") is None,
    reason="pdftotext not found (install poppler-utils)",
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


def _recipe_amounts() -> set[str]:
    gold = load_recipes()["financial_statement"].gold
    out: set[str] = set()
    for filing in gold.values():
        for key, value in filing.items():
            if key == "period":
                continue
            out.add(value)
    return out


def test_v2_file_partitions() -> None:
    cases = _load_cases()
    by_part: dict[str, int] = {}
    for case in cases:
        by_part[case["partition"]] = by_part.get(case["partition"], 0) + 1
    assert by_part["identity"] == 8
    assert by_part["neighbor"] == 8
    assert by_part["comparison"] == 6
    assert by_part["abstention"] == 4


def test_v2_numeric_gold_matches_recipe() -> None:
    allowed = _recipe_amounts()
    for case in _load_cases():
        if case["route"] == "abstain":
            continue
        if case.get("expected_value"):
            assert case["expected_value"] in allowed
        for value in case.get("expected_values") or ():
            assert value in allowed


@pytest.fixture(scope="module")
def claims():
    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext not found (install poppler-utils)")
    return extract_claims_from_dir()


@needs_pdftotext
def test_v2_identity_value_evidence(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
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


@needs_pdftotext
def test_v2_comparison_same_metric(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "comparison":
            continue
        result = lookup(case["question"], claims)
        if result.route != "identity" or not result.compare or len(result.claims) < 2:
            failures.append(f"{case['id']} compare route={result.route} n={len(result.claims)}")
            continue
        metrics = {c.metric for c in result.claims}
        scopes = {c.scope for c in result.claims}
        if len(metrics) != 1 or len(scopes) != 1:
            failures.append(f"{case['id']} mixed metric/scope {metrics} {scopes}")
        for row in result.claims:
            if not _identity_matches(case["expected_identity"], row.identity_key):
                failures.append(f"{case['id']} identity {row.identity_key}")
        values = {c.value for c in result.claims}
        if values != set(case["expected_values"]):
            failures.append(f"{case['id']} values {values}")
        periods = {c.period for c in result.claims}
        if periods != set(case["expected_periods"]):
            failures.append(f"{case['id']} periods {periods}")
    assert not failures, "\n".join(failures)


@needs_pdftotext
def test_v2_abstention(claims) -> None:
    failures: list[str] = []
    for case in _load_cases():
        if case["partition"] != "abstention":
            continue
        result = lookup(case["question"], claims)
        if result.route != "abstain" or result.claims:
            failures.append(f"{case['id']} route={result.route} claims={len(result.claims)}")
    assert not failures, "\n".join(failures)


def test_v2_harness_does_not_contact_ragflow() -> None:
    source = (ROOT / "schemas" / "finance_lines.py").read_text(encoding="utf-8").lower()
    assert "import ragflow" not in source
    assert "from ragflow" not in source
