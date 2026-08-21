"""Layer 1: MinerU artifact → FinancialStatement."""

from __future__ import annotations

from schemas.catalog import load_recipes
from schemas.classify import UNKNOWN, classify_pdf
from schemas.corpus import SAMPLES, extract_claims_from_dir
from schemas.extract import extract_financial_statement, fill_financial_statement, select_page
from schemas.parse_artifact import page_text, load_parse

PDF_1T26 = SAMPLES / "BYMA_-_EEFF_31-03-2026_VF.pdf"
PDF_2T26 = SAMPLES / "BYMA - EEFF 30-06-2026.pdf"
PDF_COMUNICADO = SAMPLES / "BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf"
PDF_MEMORIA = SAMPLES / "BYMA-MEMORIA_2024_y_EEFF_31-12-2024.pdf"


def _gold() -> dict[str, dict[str, str]]:
    return load_recipes()["financial_statement"].gold


def test_extract_1t26_matches_recipe_gold() -> None:
    gold = _gold()["BYMA_-_EEFF_31-03-2026_VF.pdf"]
    row = extract_financial_statement(PDF_1T26)
    assert row is not None
    assert row.period == gold["period"] == "2026-03-31"
    assert row.net_income_consolidated == gold["net_income_consolidated"] == "21262335"
    assert row.net_income_attributable_to_parent == gold["net_income_attributable_to_parent"] == "21259769"
    assert row.prior_period_amount_to_ignore == gold["prior_period_amount_to_ignore"] == "22362983"
    assert row.source_page == 4
    artifact = load_parse(PDF_1T26)
    assert artifact is not None
    page_digits = "".join(ch for ch in page_text(artifact, 4) if ch.isdigit())
    assert row.net_income_consolidated in page_digits
    assert row.net_income_attributable_to_parent in page_digits


def test_extract_2t26_matches_recipe_gold() -> None:
    gold = _gold()["BYMA - EEFF 30-06-2026.pdf"]
    row = extract_financial_statement(PDF_2T26)
    assert row is not None
    assert row.period == gold["period"] == "2026-06-30"
    assert row.net_income_consolidated == gold["net_income_consolidated"] == "81956525"
    assert row.net_income_attributable_to_parent == gold["net_income_attributable_to_parent"] == "81946993"
    assert row.source_page == 4


def test_page_select_uses_recipe_keywords() -> None:
    recipe = load_recipes()["financial_statement"]
    assert select_page(PDF_1T26, recipe.page_select_keywords) == 4
    assert select_page(PDF_2T26, recipe.page_select_keywords) == 4


def test_comunicado_does_not_extract_financial_statement() -> None:
    assert classify_pdf(PDF_COMUNICADO) == "press_release"
    assert extract_financial_statement(PDF_COMUNICADO) is None


def test_memoria_with_eeff_in_name_does_not_extract() -> None:
    assert classify_pdf(PDF_MEMORIA) == UNKNOWN
    assert extract_financial_statement(PDF_MEMORIA) is None


def test_extract_false_recipe_still_skips_statement() -> None:
    recipes = load_recipes()
    assert recipes["annual_report"].extract is False
    assert extract_financial_statement(PDF_MEMORIA, recipes) is None


def test_fill_rejects_invented_digits() -> None:
    fake = (
        "RESULTADO NETO DEL PERÍODO  99.999.999\n"
        "Resultado neto del período atribuible a la participación controlante  11.111.111\n"
        "31 DE MARZO DE 2026\n"
    )
    row = fill_financial_statement(fake, source_page=4, filename="BYMA_-_EEFF_fake.pdf")
    assert row is not None
    page_without = (
        "RESULTADO NETO DEL PERÍODO\n"
        "Resultado neto del período atribuible a la participación controlante\n"
        "31 DE MARZO DE 2026\n"
    )
    assert fill_financial_statement(page_without, source_page=4, filename="x.pdf") is None


def test_corpus_projects_neto_and_neighbors() -> None:
    claims = extract_claims_from_dir()
    keys = {c.identity_key for c in claims}
    gold = _gold()
    g1 = gold["BYMA_-_EEFF_31-03-2026_VF.pdf"]
    g2 = gold["BYMA - EEFF 30-06-2026.pdf"]
    by_key = {c.identity_key: c.value for c in claims}
    assert by_key["BYMA|2026-03-31|consolidado|resultado_neto"] == g1["net_income_consolidated"]
    assert by_key["BYMA|2026-03-31|controlante|resultado_atribuible_controladora"] == g1["net_income_attributable_to_parent"]
    assert by_key["BYMA|2026-03-31|consolidado|resultado_bruto"] == g1["resultado_bruto"]
    assert by_key["BYMA|2026-03-31|consolidado|resultado_operativo"] == g1["resultado_operativo"]
    assert by_key["BYMA|2026-03-31|consolidado|resultado_antes_impuesto"] == g1["resultado_antes_impuesto"]
    assert by_key["BYMA|2026-03-31|consolidado|impuesto_ganancias"] == g1["impuesto_ganancias"]
    assert by_key["BYMA|2026-03-31|consolidado|resultado_no_controlante"] == g1["resultado_no_controlante"]
    assert by_key["BYMA|2026-06-30|consolidado|resultado_bruto"] == g2["resultado_bruto"]
    assert by_key["BYMA|2026-06-30|consolidado|resultado_operativo"] == g2["resultado_operativo"]
    assert by_key["BYMA|2026-06-30|consolidado|impuesto_ganancias"] == g2["impuesto_ganancias"]
    assert by_key["BYMA|2026-06-30|consolidado|resultado_bruto"] != "58533038"
    assert keys >= {
        "BYMA|2026-03-31|consolidado|resultado_neto",
        "BYMA|2026-06-30|controlante|resultado_atribuible_controladora",
    }


def test_classify_dedicated_eeff() -> None:
    assert classify_pdf(PDF_1T26) == "financial_statement"
    assert classify_pdf(PDF_2T26) == "financial_statement"
    assert classify_pdf(PDF_MEMORIA) == UNKNOWN
    assert classify_pdf(PDF_COMUNICADO) == "press_release"
    assert classify_pdf(SAMPLES / "Presentacion_de_resultados_BYMA-2T26.pdf") == "results_presentation"
