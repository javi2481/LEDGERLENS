"""Dossier HTML: reject unpublished; gold 1T26 neto present; skip narrative."""

from __future__ import annotations

from pathlib import Path

import pytest

from schemas.claim import Claim, identity_key
from schemas.corpus import extract_claims_from_dir
from schemas.dossier import identity_qa_rows, load_eval_cases, render_dossier
from schemas.parse_artifact import fixtures_ready
from schemas.review import publishable

NETO_KEY = identity_key("BYMA", "2026-03-31", "consolidado", "resultado_neto")
NETO = Claim(
    identity_key=NETO_KEY,
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

needs_parse = pytest.mark.skipif(
    not fixtures_ready(),
    reason="missing MinerU fixtures (run scripts/export_mineru.py)",
)


def _facts_section(html: str) -> str:
    start = html.find('id="hechos"')
    if start < 0:
        start = html.find("id='hechos'")
    next_h2 = html.find("<h2", start + 1) if start >= 0 else -1
    if start < 0:
        return ""
    return html[start:next_h2] if next_h2 > start else html[start:]


def test_reject_hidden_from_facts() -> None:
    html = render_dossier((NETO, CTRL), verdicts={NETO_KEY: "reject"})
    facts = _facts_section(html)
    assert "21262335" not in facts
    assert "21259769" in facts
    assert NETO_KEY in html
    assert "reject" in html


def test_identity_qa_skips_rejected() -> None:
    cases = [
        {
            "id": "id-01",
            "route": "identity",
            "question": "neto 1T26",
            "expected_identity": NETO_KEY,
            "expected_value": "21262335",
        }
    ]
    published = publishable((NETO,), {NETO_KEY: "reject"})
    assert identity_qa_rows(cases, published) == []


def test_narrative_omitted_from_qa() -> None:
    html = render_dossier((NETO,), cases=load_eval_cases())
    assert "Explicá el crecimiento de ingresos de BYMA" not in html


def test_abstain_section_has_ypf_without_invented_value() -> None:
    html = render_dossier((NETO,), cases=load_eval_cases())
    assert "precio de cierre de YPF" in html
    abs_start = html.find("<h2>Abstenciones</h2>")
    abs_end = html.find("<h2>", abs_start + 1)
    section = html[abs_start:abs_end]
    assert "YPF" in section
    assert "21262335" not in section


def test_informe_script_does_not_import_ragflow() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "scripts" / "informe.py").read_text(encoding="utf-8")
    assert "import ragflow" not in text.lower()
    assert "from ragflow" not in text.lower()
    assert "urllib" not in text
    dossier = (root / "schemas" / "dossier.py").read_text(encoding="utf-8")
    assert "import ragflow" not in dossier.lower()
    assert "from ragflow" not in dossier.lower()


@needs_parse
def test_1t26_neto_in_dossier_when_accepted() -> None:
    claims = extract_claims_from_dir()
    html = render_dossier(claims)
    facts = _facts_section(html)
    assert "21262335" in facts
    assert NETO_KEY in facts
    assert ">4<" in facts or ">4</td>" in facts
