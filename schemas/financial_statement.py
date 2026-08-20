"""Identity-by-schema for a dedicated financial statement (EEFF).

Consolidado and controlante are two fields, not two entities to merge.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from schemas.money import digits_ars


class FinancialStatement(BaseModel):
    """P&L identity: two neighboring net-income rows stay distinct."""

    issuer: str | None = Field(
        default=None,
        description="Emisor o ticker (BYMA).",
        examples=["BYMA"],
    )
    period: str = Field(
        ...,
        description="Fecha de cierre ISO (31 de marzo de 2026 → 2026-03-31).",
        examples=["2026-03-31", "2026-06-30"],
    )
    net_income_consolidated: str | None = Field(
        default=None,
        description=(
            "RESULTADO NETO DEL PERÍODO del estado consolidado. "
            "No es la fila 'atribuible a la participación controlante'."
        ),
        examples=["21262335", "81956525"],
    )
    net_income_attributable_to_parent: str | None = Field(
        default=None,
        description=(
            "Resultado atribuible a la participación controlante / propietarios. "
            "No es RESULTADO NETO DEL PERÍODO consolidado."
        ),
        examples=["21259769", "81946993"],
    )
    source_page: int | None = Field(
        default=None,
        description="Página del P&L en este PDF (en BYMA 1T26/2T26 suele ser 4).",
        examples=[4],
    )
    source_text_consolidado: str | None = Field(
        default=None,
        description="Etiqueta literal de la fila consolidada.",
        examples=["RESULTADO NETO DEL PERÍODO"],
    )
    source_text_controlante: str | None = Field(
        default=None,
        description="Etiqueta literal de la fila controlante.",
        examples=["Resultado atribuible a la participación controlante"],
    )
    prior_period_amount_to_ignore: str | None = Field(
        default=None,
        description="Cifra de la columna del ejercicio anterior; no usar como neto.",
        examples=["22362983"],
    )

    @field_validator(
        "net_income_consolidated",
        "net_income_attributable_to_parent",
        "prior_period_amount_to_ignore",
        mode="before",
    )
    @classmethod
    def normalize_amounts(cls, v: object) -> str | None:
        return digits_ars(v)
