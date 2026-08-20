"""Second domain plugin: press release announcement date + reporting period. Not P&L."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from schemas.catalog import Recipe, load_recipes
from schemas.claim import (
    METRIC_PRESS_AS_OF,
    METRIC_PRESS_PERIOD,
    SCOPE_PRESS,
    Claim,
    identity_key,
)
from schemas.classify import UNKNOWN, classify_filename
from schemas.extract import DATE_RE, MONTHS, fold, select_page
from schemas.page_text import pdf_page_text

PERIOD_1T26 = "2026-03-31"
PERIOD_2T26 = "2026-06-30"


class PressRelease(BaseModel):
    issuer: str | None = Field(default="BYMA")
    period: str
    as_of_date: str
    source_page: int | None = None
    source_text_as_of: str | None = None
    source_text_period: str | None = None


def _iso_from_date_match(match: object) -> str:
    day, month, year = match.group(1), match.group(2), match.group(3)
    return f"{year}-{MONTHS[fold(month)]}-{int(day):02d}"


def _period_from_text_and_name(text: str, filename: str) -> tuple[str, str] | None:
    name = fold(filename)
    blob = fold(text)
    if "1t26" in name:
        return PERIOD_1T26, "1T26"
    if "2t26" in name:
        return PERIOD_2T26, "2T26"
    has_1 = "1t26" in blob
    has_2 = "2t26" in blob
    if has_1 and not has_2:
        return PERIOD_1T26, "1T26"
    if has_2 and not has_1:
        return PERIOD_2T26, "2T26"
    return None


def fill_press_release(text: str, *, source_page: int, filename: str) -> PressRelease | None:
    match = DATE_RE.search(text)
    if match is None:
        return None
    period_row = _period_from_text_and_name(text, filename)
    if period_row is None:
        return None
    period, period_label = period_row
    as_of = _iso_from_date_match(match)
    return PressRelease(
        issuer="BYMA",
        period=period,
        as_of_date=as_of,
        source_page=source_page,
        source_text_as_of=match.group(0),
        source_text_period=period_label,
    )


def claims_from_press_release(row: PressRelease) -> tuple[Claim, ...]:
    issuer = (row.issuer or "BYMA").strip() or "BYMA"
    page = row.source_page
    as_of = Claim(
        identity_key=identity_key(issuer, row.period, SCOPE_PRESS, METRIC_PRESS_AS_OF),
        value=row.as_of_date,
        period=row.period,
        source_page=page,
        source_text=row.source_text_as_of,
        issuer=issuer,
        scope=SCOPE_PRESS,
        metric=METRIC_PRESS_AS_OF,
    )
    period_claim = Claim(
        identity_key=identity_key(issuer, row.period, SCOPE_PRESS, METRIC_PRESS_PERIOD),
        value=row.period,
        period=row.period,
        source_page=page,
        source_text=row.source_text_period,
        issuer=issuer,
        scope=SCOPE_PRESS,
        metric=METRIC_PRESS_PERIOD,
    )
    return (as_of, period_claim)


def extract_press_release(pdf: Path, recipes: dict[str, Recipe] | None = None) -> PressRelease | None:
    catalog = recipes if recipes is not None else load_recipes()
    recipe_id = classify_filename(pdf.name, tuple(catalog))
    if recipe_id == UNKNOWN:
        return None
    recipe = catalog.get(recipe_id)
    if recipe is None or not recipe.extract or recipe.id != "press_release":
        return None
    page = select_page(pdf, recipe.page_select_keywords)
    if page is None:
        return None
    text = pdf_page_text(pdf, page)
    return fill_press_release(text, source_page=page, filename=pdf.name)
