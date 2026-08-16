"""Narrow BYMA EEFF overlay: resultado neto consolidado vs atribuible a la controlante."""

from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def edge(label: str, **kwargs: Any) -> Any:
    if "default" not in kwargs and "default_factory" not in kwargs:
        kwargs["default"] = None
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

    valor: Optional[str] = Field(
        None,
        description=(
            "LOOK FOR: cifra de la fila, con puntos de miles AR (21.262.335). "
            "Copiar dígitos; no redondear ni sumar. Normalizar quitando puntos de miles."
        ),
        examples=["21262335", "21259769"],
    )
    unidad: Optional[str] = Field(
        None,
        description="LOOK FOR: miles de pesos / ARS / $ en el encabezado. Copiar; no convertir.",
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
    """Emisor del EEFF, identificado por CUIT impreso."""

    model_config = ConfigDict(graph_id_fields=["cuit"])

    cuit: str = Field(
        ...,
        description="LOOK FOR: CUIT (NN-NNNNNNNN-N) en carátula o notas. Copiar tal cual.",
        examples=["30-71547195-3"],
    )
    nombre: Optional[str] = Field(
        None,
        description="LOOK FOR: razón social (Bolsas y Mercados Argentinos / BYMA).",
        examples=["Bolsas y Mercados Argentinos S.A."],
    )


class HechoFinanciero(BaseModel):
    """Una cifra de la síntesis: neto consolidado O atribuible a la controlante. Otras filas del P&L no son hechos."""

    model_config = ConfigDict(
        graph_id_fields=["hecho_id"],
        graph_max_instances=8,
    )

    hecho_id: str = Field(
        ...,
        description=(
            "Id derivado: cuit|YYYY-MM-DD|consolidado|resultado_neto "
            "o ...|controlante|resultado_atribuible_controladora. "
            "Copiar CUIT, fecha de cierre y estado del encabezado; no inventar códigos."
        ),
        examples=[
            "30-71547195-3|2026-03-31|consolidado|resultado_neto",
            "30-71547195-3|2026-03-31|controlante|resultado_atribuible_controladora",
        ],
    )
    periodo: Optional[str] = Field(
        None,
        description="LOOK FOR: 31 de marzo de 2026 → 2026-03-31. No usar 1T26 si el PDF trae fecha.",
        examples=["2026-03-31"],
    )
    estado: Optional[EstadoEEFF] = Field(
        None,
        description=(
            "consolidado = columna/encabezado consolidada. "
            "controlante = atribuible a los propietarios / sociedad controlante. "
            "Conviven en la misma página; no fusionar."
        ),
    )
    metrica: Optional[MetricaEEFF] = Field(
        None,
        description=(
            "resultado_neto = RESULTADO NETO DEL PERÍODO (consolidado). "
            "resultado_atribuible_controladora = atribuible a propietarios de la controlante."
        ),
    )
    monto: Optional[Monto] = edge(label="HAS_AMOUNT")
    fuente_pagina: Optional[int] = Field(
        None,
        description="LOOK FOR: número de página impresa de la síntesis. Omitir si no está.",
        examples=[1, 2],
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
        description="LOOK FOR: título de carátula (Estados Financieros … 31 de marzo de 2026).",
        examples=["Estados Financieros condensados al 31 de marzo de 2026"],
    )
    emisor: Optional[Emisor] = edge(label="ISSUED_BY")
    hechos: List[HechoFinanciero] = edge(
        label="REPORTS_FACT",
        default_factory=list,
        description="Solo las dos líneas de la síntesis (neto consolidado y atribuible controlante).",
    )
