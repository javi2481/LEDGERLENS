"""Typed claim: domain-agnostic identity + value + provenance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Route = Literal["identity", "abstain", "narrative"]

SCOPE_CONSOLIDADO = "consolidado"
SCOPE_CONTROLANTE = "controlante"
METRIC_NETO = "resultado_neto"
METRIC_ATRIBUIBLE = "resultado_atribuible_controladora"


def identity_key(issuer: str, period: str, scope: str, metric: str) -> str:
    return f"{issuer}|{period}|{scope}|{metric}"


@dataclass(frozen=True)
class Claim:
    identity_key: str
    value: str
    period: str
    source_page: int | None
    source_text: str | None
    issuer: str | None = None
    scope: str | None = None
    metric: str | None = None


def claims_from_financial_statement(row: object) -> tuple[Claim, ...]:
    """Project the finance plugin DTO into two claims. Other domains add their own projector."""
    from schemas.financial_statement import FinancialStatement

    if not isinstance(row, FinancialStatement):
        raise TypeError("finance projector expects FinancialStatement")
    issuer = (row.issuer or "BYMA").strip() or "BYMA"
    period = row.period
    page = row.source_page
    consolidado = Claim(
        identity_key=identity_key(issuer, period, SCOPE_CONSOLIDADO, METRIC_NETO),
        value=row.net_income_consolidated or "",
        period=period,
        source_page=page,
        source_text=row.source_text_consolidado,
        issuer=issuer,
        scope=SCOPE_CONSOLIDADO,
        metric=METRIC_NETO,
    )
    controlante = Claim(
        identity_key=identity_key(issuer, period, SCOPE_CONTROLANTE, METRIC_ATRIBUIBLE),
        value=row.net_income_attributable_to_parent or "",
        period=period,
        source_page=page,
        source_text=row.source_text_controlante,
        issuer=issuer,
        scope=SCOPE_CONTROLANTE,
        metric=METRIC_ATRIBUIBLE,
    )
    return (consolidado, controlante)
