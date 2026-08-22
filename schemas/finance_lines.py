"""Finance plugin: closed P&L neighbor lines. Not kernel; not a fatter FinancialStatement."""

from __future__ import annotations

import re
from dataclasses import dataclass

from schemas.claim import (
    METRIC_BRUTO,
    METRIC_EBT,
    METRIC_IMPUESTO,
    METRIC_NCI,
    METRIC_OPERATIVO,
    SCOPE_CONSOLIDADO,
    Claim,
    identity_key,
)
from schemas.extract import fold
from schemas.financial_statement import FinancialStatement
from schemas.money import signed_ars

SIGNED_AMOUNT_RE = re.compile(r"\(?\d{1,3}(?:\.\d{3})+\)?")


@dataclass(frozen=True)
class LineSpec:
    metric: str
    include: tuple[str, ...]
    exclude: tuple[str, ...] = ()


PNL_LINES: tuple[LineSpec, ...] = (
    LineSpec(METRIC_BRUTO, ("resultado bruto",), ("operativo", "neto", "impuesto")),
    LineSpec(METRIC_OPERATIVO, ("resultado operativo",), ("financiero", "neto", "bruto")),
    LineSpec(METRIC_EBT, ("antes del impuesto",), ("neto",)),
    LineSpec(METRIC_IMPUESTO, ("impuesto a las ganancias",), ("antes", "neto")),
    LineSpec(METRIC_NCI, ("no controlante",), ("accionistas",)),
)


def _signed_amounts(line: str) -> list[str]:
    found: list[str] = []
    for raw in SIGNED_AMOUNT_RE.findall(line):
        parsed = signed_ars(raw)
        if parsed:
            found.append(parsed)
    return found


def _label_before_amount(line: str) -> str:
    match = SIGNED_AMOUNT_RE.search(line)
    label = line[: match.start()] if match else line
    return " ".join(label.split())


def _line_matches(line: str, spec: LineSpec) -> bool:
    blob = fold(line)
    if not all(token in blob for token in spec.include):
        return False
    if any(token in blob for token in spec.exclude):
        return False
    return True


def claims_from_pnl_lines(page_text: str, row: FinancialStatement) -> tuple[Claim, ...]:
    issuer = (row.issuer or "").strip()
    if not issuer:
        return ()
    period = row.period
    page = row.source_page
    page_digits = "".join(ch for ch in page_text if ch.isdigit())
    out: list[Claim] = []
    for spec in PNL_LINES:
        matched = ""
        for raw in page_text.splitlines():
            line = raw.strip()
            if line and _line_matches(line, spec):
                matched = line
                break
        if not matched:
            continue
        amounts = _signed_amounts(matched)
        if not amounts:
            continue
        value = amounts[0]
        digits = value.lstrip("-")
        if digits not in page_digits:
            continue
        out.append(
            Claim(
                identity_key=identity_key(issuer, period, SCOPE_CONSOLIDADO, spec.metric),
                value=value,
                period=period,
                source_page=page,
                source_text=_label_before_amount(matched),
                issuer=issuer,
                scope=SCOPE_CONSOLIDADO,
                metric=spec.metric,
            )
        )
    return tuple(out)
