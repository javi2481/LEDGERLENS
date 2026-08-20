"""Ola 1: schema catalog and identity contract. No Docker."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from schemas.catalog import classifier_labels, load_recipes
from schemas.financial_statement import FinancialStatement
from schemas.money import digits_ars
from schemas.validate import reject_financial_statement


def test_catalog_covers_sample_types() -> None:
    recipes = load_recipes()
    assert set(recipes) >= {
        "financial_statement",
        "press_release",
        "results_presentation",
        "earnings_transcript",
        "annual_report",
        "legal_contract",
    }
    assert recipes["financial_statement"].extract is True
    assert recipes["financial_statement"].schema_cls() is FinancialStatement
    for rid in (
        "press_release",
        "results_presentation",
        "earnings_transcript",
        "annual_report",
        "legal_contract",
    ):
        assert recipes[rid].extract is False
        assert recipes[rid].schema_cls() is None
    labels = classifier_labels(recipes)
    assert labels[-1] == "UNKNOWN"
    assert "financial_statement" in labels


def test_digits_ars() -> None:
    assert digits_ars("21.262.335") == "21262335"
    assert digits_ars("81.956.525") == "81956525"
    assert digits_ars(None) is None


def test_signed_ars_parentheses() -> None:
    from schemas.money import signed_ars

    assert signed_ars("(14.950.948)") == "-14950948"
    assert signed_ars("60.144.176") == "60144176"
    assert signed_ars(None) is None


def test_identity_gold_1t26() -> None:
    gold = load_recipes()["financial_statement"].gold["BYMA_-_EEFF_31-03-2026_VF.pdf"]
    row = FinancialStatement(
        issuer="BYMA",
        period=gold["period"],
        net_income_consolidated=gold["net_income_consolidated"],
        net_income_attributable_to_parent=gold["net_income_attributable_to_parent"],
        prior_period_amount_to_ignore=gold["prior_period_amount_to_ignore"],
        source_page=4,
    )
    assert reject_financial_statement(row) is None
    assert row.net_income_consolidated != row.net_income_attributable_to_parent
    assert row.net_income_consolidated != row.prior_period_amount_to_ignore


def test_identity_gold_2t26() -> None:
    gold = load_recipes()["financial_statement"].gold["BYMA - EEFF 30-06-2026.pdf"]
    row = FinancialStatement(
        period=gold["period"],
        net_income_consolidated=gold["net_income_consolidated"],
        net_income_attributable_to_parent=gold["net_income_attributable_to_parent"],
    )
    assert reject_financial_statement(row) is None


def test_abstain_same_amount() -> None:
    row = FinancialStatement(
        period="2026-03-31",
        net_income_consolidated="21262335",
        net_income_attributable_to_parent="21262335",
    )
    assert reject_financial_statement(row) == "consolidado equals controlante"


def test_abstain_missing_controlante() -> None:
    row = FinancialStatement(period="2026-03-31", net_income_consolidated="21262335")
    assert reject_financial_statement(row) == "missing consolidado or controlante"


def test_printed_dots_normalize() -> None:
    row = FinancialStatement(
        period="2026-03-31",
        net_income_consolidated="21.262.335",
        net_income_attributable_to_parent="21.259.769",
    )
    assert row.net_income_consolidated == "21262335"
    assert row.net_income_attributable_to_parent == "21259769"
    assert reject_financial_statement(row) is None
