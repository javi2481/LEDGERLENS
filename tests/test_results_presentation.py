"""Results presentation: EBITDA + LTM margin from MinerU highlights. Not P&L."""

from __future__ import annotations

from schemas.catalog import load_recipes
from schemas.classify import classify_pdf
from schemas.corpus import SAMPLES, extract_claims_from_dir
from schemas.extract import extract_financial_statement
from schemas.results_presentation import extract_results_presentation

PDF_1T26 = SAMPLES / "Presentación_de_resultados_BYMA-1T26.pdf"
PDF_2T26 = SAMPLES / "Presentacion_de_resultados_BYMA-2T26.pdf"
PDF_MEMORIA = SAMPLES / "BYMA-MEMORIA_2024_y_EEFF_31-12-2024.pdf"


def test_extract_decks_match_recipe_gold() -> None:
    gold = load_recipes()["results_presentation"].gold
    row_1 = extract_results_presentation(PDF_1T26)
    row_2 = extract_results_presentation(PDF_2T26)
    assert row_1 is not None and row_2 is not None
    g1 = gold[PDF_1T26.name]
    g2 = gold[PDF_2T26.name]
    assert row_1.ebitda == g1["presentation_ebitda"] == "72128"
    assert row_1.ebitda_margin_ltm == g1["presentation_ebitda_margin_ltm"] == "76"
    assert row_1.period == g1["period"] == "2026-03-31"
    assert row_1.source_page == 12
    assert row_2.ebitda == g2["presentation_ebitda"] == "71697"
    assert row_2.ebitda_margin_ltm == g2["presentation_ebitda_margin_ltm"] == "75"
    assert row_2.period == g2["period"] == "2026-06-30"
    assert extract_financial_statement(PDF_1T26) is None
    assert extract_financial_statement(PDF_MEMORIA) is None


def test_classify_deck_is_results_presentation() -> None:
    assert classify_pdf(PDF_1T26) == "results_presentation"
    assert classify_pdf(PDF_2T26) == "results_presentation"


def test_presentation_claims_are_not_pnl() -> None:
    claims = extract_claims_from_dir()
    deck = [c for c in claims if c.scope == "presentacion"]
    assert deck
    assert {c.metric for c in deck} <= {
        "presentation_ebitda",
        "presentation_ebitda_margin_ltm",
    }
    assert not any(
        c.scope == "presentacion" and c.metric in {"resultado_neto", "impuesto_ganancias"}
        for c in claims
    )
