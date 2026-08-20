"""Layer 2: lexical identity lookup. No RAGFlow."""

from __future__ import annotations

import shutil

import pytest

from schemas.claim import SCOPE_CONSOLIDADO, SCOPE_CONTROLANTE
from schemas.corpus import extract_claims_from_dir
from schemas.lookup import lookup, understand

needs_pdftotext = pytest.mark.skipif(
    shutil.which("pdftotext") is None,
    reason="pdftotext not found (install poppler-utils)",
)


@pytest.fixture(scope="module")
def claims():
    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext not found (install poppler-utils)")
    return extract_claims_from_dir()


def test_default_consolidado_trap(claims) -> None:
    result = lookup("¿Cuál es el resultado neto del período 1T26?", claims)
    assert result.route == "identity"
    assert len(result.claims) == 1
    row = result.claims[0]
    assert row.scope == SCOPE_CONSOLIDADO
    assert row.value == "21262335"
    assert row.value != "21259769"
    assert row.value != "22362983"
    assert row.source_page == 4
    assert row.source_text


def test_explicit_controlante(claims) -> None:
    result = lookup("Resultado atribuible a la participación controlante 1T26", claims)
    assert result.route == "identity"
    assert result.claims[0].scope == SCOPE_CONTROLANTE
    assert result.claims[0].value == "21259769"


def test_no_controlante_is_not_neto(claims) -> None:
    result = lookup("Resultado atribuible a la participación no controlante 1T26", claims)
    assert result.route == "identity"
    row = result.claims[0]
    assert row.metric == "resultado_no_controlante"
    assert row.value == "2566"
    assert row.value != "21262335"
    assert row.value != "21259769"


def test_bruto_not_operativo(claims) -> None:
    result = lookup("¿Cuál es el resultado bruto del 1T26?", claims)
    assert result.route == "identity"
    assert result.claims[0].value == "60144176"
    assert result.claims[0].value != "70223471"
    assert result.claims[0].value != "21262335"


def test_compare_same_identity(claims) -> None:
    result = lookup("Comparar resultado neto consolidado 1T26 vs 2T26", claims)
    assert result.route == "identity"
    assert result.compare is True
    scopes = {c.scope for c in result.claims}
    assert scopes == {SCOPE_CONSOLIDADO}
    values = {c.value for c in result.claims}
    assert values == {"21262335", "81956525"}
    assert "21259769" not in values
    assert "81946993" not in values


def test_ypf_abstains(claims) -> None:
    result = lookup("¿Cuál fue el precio de cierre de YPF en BYMA el 3 de enero?", claims)
    assert result.route == "abstain"
    assert result.claims == ()


def test_press_date_not_pnl(claims) -> None:
    result = lookup("¿Cuál es la fecha del comunicado de prensa 1T26?", claims)
    assert result.route == "identity"
    row = result.claims[0]
    assert row.metric == "press_as_of_date"
    assert row.value == "2026-05-08"
    assert row.value != "21262335"


def test_eeff_metric_on_comunicado_still_abstains(claims) -> None:
    result = lookup("¿Cuál es el resultado neto consolidado del comunicado de prensa?", claims)
    assert result.route == "abstain"
    assert result.claims == ()


def test_understand_narrative_is_not_identity() -> None:
    intent = understand("Explicá el crecimiento de ingresos de BYMA")
    assert intent.route == "narrative"


def test_no_ragflow_import() -> None:
    import inspect

    import schemas.extract as extract_mod
    import schemas.lookup as lookup_mod

    for module in (lookup_mod, extract_mod):
        source = inspect.getsource(module)
        assert "ragflow" not in source.lower()
        assert "voyage" not in source.lower()
        assert "infinity" not in source.lower()
