"""Narrow BYMA EEFF overlay: resultado neto consolidado vs atribuible a la controlante."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


def edge(label: str, **kwargs: Any) -> Any:
    return Field(json_schema_extra={"edge_label": label}, **kwargs)


class EstadoEEFF(str, Enum):
    consolidado = "consolidado"
    controlante = "controlante"


class MetricaEEFF(str, Enum):
    resultado_neto = "resultado_neto"
    resultado_atribuible_controladora = "resultado_atribuible_controladora"


class Monto(BaseModel):
    """Importe copiado digit-for-digit. No es entidad."""

    model_config = ConfigDict(is_entity=False)

    valor: str = Field(
        ...,
        description=(
            "Cifra de la fila, puntos de miles AR (21.262.335). "
            "Copiar dígitos; no redondear. Quitar puntos de miles."
        ),
        examples=["21262335", "21259769"],
    )
    unidad: str = Field(
        default="ARS",
        description="Unidad del encabezado (miles de pesos / ARS). Copiar; no convertir.",
        examples=["ARS", "miles de pesos"],
    )

    @field_validator("valor", mode="before")
    @classmethod
    def strip_thousands(cls, v: Any) -> Any:
        if v is None:
            return v
        text = str(v).strip().replace(" ", "")
        if text.count(".") >= 1 and "," not in text:
            parts = text.split(".")
            if all(p.isdigit() for p in parts) and all(len(p) == 3 for p in parts[1:]):
                return "".join(parts)
        return text.replace(".", "") if text.replace(".", "").isdigit() else text


class Emisor(BaseModel):
    """Emisor del EEFF. En la página del P&L puede no haber CUIT."""

    model_config = ConfigDict(graph_id_fields=["nombre"])

    nombre: str = Field(
        ...,
        description="Razón social o ticker (BYMA / Bolsas y Mercados Argentinos).",
        examples=["BYMA"],
    )
    cuit: str = Field(
        default="",
        description="CUIT NN-NNNNNNNN-N si está impreso. Vacío si no aparece en esta página.",
        examples=["30-71547195-3"],
    )


class HechoFinanciero(BaseModel):
    """Una sola línea del P&L: neto consolidado O atribuible a la controlante."""

    model_config = ConfigDict(
        graph_id_fields=["hecho_id"],
        graph_max_instances=2,
    )

    hecho_id: str = Field(
        ...,
        description=(
            "Id: BYMA|YYYY-MM-DD|consolidado|resultado_neto "
            "o BYMA|YYYY-MM-DD|controlante|resultado_atribuible_controladora."
        ),
        examples=[
            "BYMA|2026-03-31|consolidado|resultado_neto",
            "BYMA|2026-03-31|controlante|resultado_atribuible_controladora",
        ],
    )
    periodo: str = Field(
        ...,
        description="Fecha de cierre ISO. 31 de marzo de 2026 → 2026-03-31.",
        examples=["2026-03-31"],
    )
    estado: EstadoEEFF = Field(
        ...,
        description=(
            "consolidado = RESULTADO NETO DEL PERÍODO (21.262.335). "
            "controlante = atribuible a la participación controlante (21.259.769)."
        ),
    )
    metrica: MetricaEEFF = Field(
        ...,
        description=(
            "resultado_neto = RESULTADO NETO DEL PERÍODO. "
            "resultado_atribuible_controladora = atribuible a la participación controlante."
        ),
    )
    monto: Monto = edge(label="HAS_AMOUNT")
    fuente_pagina: int = Field(
        ...,
        description="Número de página del PDF (esta hoja es la 4).",
        examples=[4],
    )

    @field_validator("hecho_id", mode="before")
    @classmethod
    def strip_id(cls, v: Any) -> Any:
        return str(v).strip() if v is not None else v


class EeffByma(BaseModel):
    """EEFF BYMA de un cierre. No es comunicado ni presentación."""

    model_config = ConfigDict(graph_id_fields=["titulo"])

    titulo: str = Field(
        ...,
        description="Título del estado (Estados Financieros condensados / RESULTADO).",
        examples=["Estado de resultados consolidado al 31 de marzo de 2026"],
    )
    emisor: Emisor | None = edge(label="ISSUED_BY", default=None)
    resultado_neto_consolidado: HechoFinanciero = edge(label="REPORTS_CONSOLIDADO")
    resultado_atribuible_controlante: HechoFinanciero = edge(label="REPORTS_CONTROLANTE")
