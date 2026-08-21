"""Press-release plugin: date + period from MinerU artifact. Not P&L."""

from __future__ import annotations

import json
from pathlib import Path

from schemas.catalog import load_recipes
from schemas.classify import classify_pdf
from schemas.corpus import SAMPLES, extract_claims_from_dir
from schemas.extract import extract_financial_statement
from schemas.press_release import extract_press_release

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "press_v1.json"
PDF_1T26 = SAMPLES / "BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf"
PDF_2T26 = SAMPLES / "BYMA-Comunicado_de_Prensa-2T26.pdf"


def _gold() -> dict[str, dict[str, str]]:
    return load_recipes()["press_release"].gold


def test_extract_comunicados_match_recipe_gold() -> None:
    gold = _gold()
    row_1 = extract_press_release(PDF_1T26)
    row_2 = extract_press_release(PDF_2T26)
    assert row_1 is not None and row_2 is not None
    g1 = gold[PDF_1T26.name]
    g2 = gold[PDF_2T26.name]
    assert row_1.as_of_date == g1["press_as_of_date"] == "2026-05-08"
    assert row_1.period == g1["press_period"] == "2026-03-31"
    assert row_1.ebitda_margin_ltm == g1["press_ebitda_margin_ltm"] == "76"
    assert row_1.source_page_ltm == 2
    assert row_2.as_of_date == g2["press_as_of_date"] == "2026-08-07"
    assert row_2.period == g2["press_period"] == "2026-06-30"
    assert row_2.ebitda_margin_ltm == g2["press_ebitda_margin_ltm"] == "75"
    assert row_2.source_page_ltm == 2
    assert extract_financial_statement(PDF_1T26) is None
    assert extract_financial_statement(PDF_2T26) is None


def test_classify_comunicado_is_press_release() -> None:
    assert classify_pdf(PDF_1T26) == "press_release"
    assert classify_pdf(PDF_2T26) == "press_release"


def test_press_claims_are_not_pnl_metrics() -> None:
    claims = extract_claims_from_dir()
    press = [c for c in claims if c.scope == "comunicado"]
    assert press
    assert {c.metric for c in press} <= {
        "press_as_of_date",
        "press_period",
        "press_ebitda_margin_ltm",
    }
    assert not any(
        c.metric in {"resultado_neto", "impuesto_ganancias"} and c.scope == "comunicado" for c in claims
    )


def test_eval_file_exists() -> None:
    payload = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    assert payload["gold_ref"] == "recipes/press_release.json"
    assert len(payload["cases"]) >= 9


def test_press_ltm_matches_presentation_gold() -> None:
    press_1 = extract_press_release(PDF_1T26)
    press_2 = extract_press_release(PDF_2T26)
    deck_gold = load_recipes()["results_presentation"].gold
    assert press_1 is not None and press_2 is not None
    assert (
        press_1.ebitda_margin_ltm
        == deck_gold["Presentación_de_resultados_BYMA-1T26.pdf"]["presentation_ebitda_margin_ltm"]
        == "76"
    )
    assert (
        press_2.ebitda_margin_ltm
        == deck_gold["Presentacion_de_resultados_BYMA-2T26.pdf"]["presentation_ebitda_margin_ltm"]
        == "75"
    )
    claims = extract_claims_from_dir()
    press_keys = {c.identity_key for c in claims if c.metric == "press_ebitda_margin_ltm"}
    deck_keys = {c.identity_key for c in claims if c.metric == "presentation_ebitda_margin_ltm"}
    assert press_keys
    assert deck_keys
    assert press_keys.isdisjoint(deck_keys)

