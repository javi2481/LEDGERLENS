"""Format kernel claims for RAGFlow chunk + prompt inject. Not identity gold."""

from __future__ import annotations

import re
from collections.abc import Iterable

from schemas.claim import (
    METRIC_ATRIBUIBLE,
    METRIC_NETO,
    SCOPE_CONSOLIDADO,
    SCOPE_CONTROLANTE,
    Claim,
)
from schemas.classify import dedicated_financial_statement
from schemas.money import format_display_ars

MARKER = "Ficha IDP"
MARKER_GRAPH = "Ficha Graph EEFF"
# Prompt chrome. Keep "claimprint" in markers so a live RAGFlow chat
# from the old inject still matches on upsert.
IDP_START = "--- Fichas IDP (claimprint) ---"
IDP_END = "--- Fin fichas IDP ---"
GRAPH_START = "--- Fichas Graph (claimprint) ---"
GRAPH_END = "--- Fin fichas Graph ---"
SIDECAR_NAMES = ("hechos_eeff.md",)

MONEY_METRICS = {
    METRIC_NETO,
    METRIC_ATRIBUIBLE,
    "resultado_bruto",
    "resultado_operativo",
    "resultado_antes_impuesto",
    "impuesto_ganancias",
    "resultado_no_controlante",
    "presentation_ebitda",
}

IDP_RULES = (
    "Si el conocimiento incluye un bloque «Ficha IDP», esas cifras tienen "
    "prioridad sobre otras filas de la misma tabla del PDF. Distinguí consolidado "
    "(RESULTADO NETO DEL PERÍODO del estado consolidado) vs controlante "
    "(atribuible a la participación controlante / propietarios). Si la pregunta "
    "pide resultado neto / el período / un trimestre y no dice controlante ni "
    "atribuible, usá el consolidado de la ficha. Si pide controlante / atribuible / "
    "propietarios, usá esa fila. Si hay dos filas vecinas, no elijas la de al lado. "
    "Ignorá la columna del ejercicio anterior. Justificá con una cita del PDF del "
    "estado (Show Quote). No cites un markdown auxiliar ni hechos_eeff.md."
)


def display_value(claim: Claim) -> str:
    if claim.metric in MONEY_METRICS:
        return format_display_ars(claim.value)
    return claim.value


def claim_of(
    claims: Iterable[Claim],
    *,
    period: str,
    scope: str,
    metric: str,
) -> Claim | None:
    for claim in claims:
        if claim.period == period and claim.scope == scope and claim.metric == metric:
            return claim
    return None


def needs_eeff_chunk(name: str) -> bool:
    return dedicated_financial_statement(name)


def eeff_chunk(claims: tuple[Claim, ...] | list[Claim], period: str) -> tuple[str, list[str], list[str]] | None:
    consolidado = claim_of(claims, period=period, scope=SCOPE_CONSOLIDADO, metric=METRIC_NETO)
    controlante = claim_of(claims, period=period, scope=SCOPE_CONTROLANTE, metric=METRIC_ATRIBUIBLE)
    if consolidado is None or controlante is None:
        return None
    cons = display_value(consolidado)
    ctrl = display_value(controlante)
    page = consolidado.source_page or 4
    content = (
        f"{MARKER} — síntesis de la estructura de resultados consolidada, página {page}, "
        f"EEFF al {period}.\n"
        f"RESULTADO NETO DEL PERÍODO (estado consolidado): {cons}.\n"
        f"Resultado atribuible a la participación controlante: {ctrl}.\n"
        f"Si la pregunta pide el resultado neto del período o consolidado sin decir "
        f"controlante, la cifra es {cons}. {ctrl} es la fila de al lado (controlante)."
    )
    keywords = ["consolidado", "controlante", "RESULTADO NETO", cons, ctrl, period]
    questions = [
        f"Cuál es el RESULTADO NETO DEL PERÍODO al {period}",
        f"Resultado atribuible a la participación controlante al {period}",
    ]
    return content, keywords, questions


def prompt_lines(claims: tuple[Claim, ...] | list[Claim]) -> str:
    rows = list(claims)
    if not rows:
        return IDP_RULES
    lines = [IDP_RULES, "Fichas de este corpus:"]
    by_period: dict[str, list[Claim]] = {}
    for claim in rows:
        by_period.setdefault(claim.period, []).append(claim)
    for period in sorted(by_period):
        bits: list[str] = []
        for claim in by_period[period]:
            label = f"{claim.scope or '?'}|{claim.metric or '?'}"
            bits.append(f"{label} {display_value(claim)}")
        page = next((c.source_page for c in by_period[period] if c.source_page), None)
        page_bit = f", página {page}" if page else ""
        lines.append(f"- {period}{page_bit}: " + "; ".join(bits) + ".")
    return "\n".join(lines)


def upsert_idp_prompt(system: str, block: str) -> str:
    wrapped = f"{IDP_START}\n{block}\n{IDP_END}"
    text = system or ""
    text = re.sub(
        re.escape(IDP_START) + r".*?" + re.escape(IDP_END) + r"\n?",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        re.escape(GRAPH_START) + r".*?" + re.escape(GRAPH_END) + r"\n?",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"FICHAS GRAPH \(identidad.*?(?=\nEres un asistente|\nAquí está la base)",
        "",
        text,
        flags=re.S,
    )
    if "{knowledge}" in text:
        return text.replace("{knowledge}", wrapped + "\n{knowledge}", 1)
    if text.strip():
        return wrapped + "\n" + text
    return (
        "Responde solo en español. Cita los fragmentos. Si no hay evidencia, usa la "
        "respuesta vacía. No inventes cifras.\n"
        f"{wrapped}\n"
        "Eres un asistente inteligente. Resume el contenido de la base de conocimiento "
        "para responder la pregunta. Enumera los datos de la base de conocimiento y "
        "responde con detalle. Cuando todo el contenido de la base de conocimiento sea "
        "irrelevante para la pregunta, tu respuesta debe incluir la frase "
        '"No hay evidencia suficiente en los documentos indexados para responder. '
        'No invento datos.". Las respuestas necesitan considerar el historial de chat.\n'
        "Aquí está la base de conocimiento:\n{knowledge}\n"
        "Esa es la base de conocimiento."
    )


def is_inject_chunk(text: str) -> bool:
    return MARKER in text or MARKER_GRAPH in text
