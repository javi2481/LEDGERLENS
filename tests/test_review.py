"""HITL verdicts: default accept; reject unpublished; flag annex-only."""

from __future__ import annotations

import json
from pathlib import Path

from schemas.claim import Claim, identity_key
from schemas.review import (
    flagged,
    load_verdicts,
    publishable,
    render_review_html,
    rejected,
)

NETO = Claim(
    identity_key=identity_key("BYMA", "2026-03-31", "consolidado", "resultado_neto"),
    value="21262335",
    period="2026-03-31",
    source_page=4,
    source_text="RESULTADO NETO DEL PERÍODO",
    issuer="BYMA",
    scope="consolidado",
    metric="resultado_neto",
)
CTRL = Claim(
    identity_key=identity_key(
        "BYMA", "2026-03-31", "controlante", "resultado_atribuible_controladora"
    ),
    value="21259769",
    period="2026-03-31",
    source_page=4,
    source_text="participación controlante",
    issuer="BYMA",
    scope="controlante",
    metric="resultado_atribuible_controladora",
)


def test_missing_file_is_accept_all(tmp_path: Path) -> None:
    assert load_verdicts(tmp_path / "missing.json") == {}
    assert publishable((NETO, CTRL), {}) == (NETO, CTRL)
    assert publishable((NETO, CTRL), None) == (NETO, CTRL)


def test_reject_is_unpublished(tmp_path: Path) -> None:
    path = tmp_path / "v.json"
    path.write_text(
        json.dumps({"verdicts": {NETO.identity_key: "reject"}}),
        encoding="utf-8",
    )
    verdicts = load_verdicts(path)
    pub = publishable((NETO, CTRL), verdicts)
    assert CTRL in pub
    assert NETO not in pub
    assert rejected((NETO, CTRL), verdicts) == (NETO,)


def test_flag_is_annex_only() -> None:
    verdicts = {CTRL.identity_key: "flag"}
    assert publishable((NETO, CTRL), verdicts) == (NETO,)
    assert flagged((NETO, CTRL), verdicts) == (CTRL,)


def test_corrupt_json_is_accept_all(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_verdicts(path) == {}


def test_review_html_includes_key_and_source() -> None:
    html = render_review_html((NETO,))
    assert NETO.identity_key in html
    assert "RESULTADO NETO DEL PERÍODO" in html
    assert "21262335" in html


def test_example_verdicts_are_all_accept() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = json.loads(
        (root / "examples" / "review_verdicts.example.json").read_text(encoding="utf-8")
    )
    assert len(payload["verdicts"]) == 22
    assert set(payload["verdicts"].values()) == {"accept"}
