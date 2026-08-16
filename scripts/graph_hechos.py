"""Shared Graph EEFF helpers. Not a service; used by overlay scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path

MARKER = "Ficha Graph EEFF"
GRAPH_START = "--- Fichas Graph (LedgerLens) ---"
GRAPH_END = "--- Fin fichas Graph ---"
CATALOG = Path(__file__).resolve().parents[1] / "docs" / "hechos_eeff.json"
OUTPUTS = Path(__file__).resolve().parents[1] / "outputs"
SIDECAR = "hechos_eeff.md"

SKIP_SUBSTR = (
    "memoria",
    "comunicado",
    "presentacion",
    "presentación",
    "transcripcion",
    "transcripción",
)

GRAPH_RULES = (
    "Si el conocimiento incluye un bloque «Ficha Graph EEFF», esas cifras tienen "
    "prioridad sobre otras filas de la misma tabla del PDF. Distinguí consolidado "
    "(RESULTADO NETO DEL PERÍODO del estado consolidado) vs controlante "
    "(atribuible a la participación controlante / propietarios). Si la pregunta "
    "pide resultado neto / el período / un trimestre y no dice controlante ni "
    "atribuible, usá el consolidado de la ficha. Si pide controlante / atribuible / "
    "propietarios, usá esa fila. Si hay dos filas vecinas, no elijas la de al lado. "
    "Ignorá la columna del ejercicio anterior. Justificá con una cita del PDF del "
    "estado (Show Quote). No cites hechos_eeff.md ni un markdown auxiliar."
)


def needs_graph(name: str) -> bool:
    """Dedicated EEFF filings. Memorias/comunicados/presentaciones are not auto-Graph."""
    lower = name.lower()
    if not lower.endswith(".pdf"):
        return False
    if "eeff" not in lower:
        return False
    return not any(token in lower for token in SKIP_SUBSTR)


def format_ars(value: str) -> str:
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return str(value)
    parts: list[str] = []
    while digits:
        parts.append(digits[-3:])
        digits = digits[:-3]
    return ".".join(reversed(parts))


def load_catalog(path: Path | None = None) -> list[dict]:
    src = path or CATALOG
    if not src.is_file():
        return []
    payload = json.loads(src.read_text(encoding="utf-8"))
    rows = payload.get("fichas") if isinstance(payload, dict) else payload
    return [row for row in (rows or []) if isinstance(row, dict) and row.get("name")]


def load_output_fichas() -> list[dict]:
    found: list[dict] = []
    if not OUTPUTS.is_dir():
        return found
    for ficha in OUTPUTS.glob("*/ficha.json"):
        try:
            row = json.loads(ficha.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("name"):
            found.append(row)
    return found


def merge_fichas(catalog: list[dict], extra: list[dict]) -> list[dict]:
    by_name: dict[str, dict] = {}
    for row in catalog + extra:
        name = row.get("name")
        if name:
            by_name[name] = row
    return list(by_name.values())


def ficha_chunk(row: dict, compare_labels: list[str]) -> tuple[str, list[str], list[str]]:
    consolidado = format_ars(row["consolidado"])
    controlante = format_ars(row["controlante"])
    label = row.get("label") or ""
    cierre = row.get("cierre") or row.get("periodo") or ""
    pagina = row.get("pagina") or 4
    notas = row.get("notas") or ""
    no_usar = [format_ars(x) for x in (row.get("no_usar") or [])]
    extra = ""
    if no_usar:
        extra = f" No usar {', '.join(no_usar)} (ejercicio anterior u otra columna)."
    if notas:
        extra += f" {notas}."
    content = (
        f"{MARKER} — síntesis de la estructura de resultados consolidada, página {pagina}, "
        f"EEFF al {cierre} ({label}).\n"
        f"RESULTADO NETO DEL PERÍODO (estado consolidado): {consolidado}.\n"
        f"Resultado atribuible a la participación controlante: {controlante}.\n"
        f"Si la pregunta pide el resultado neto del período o consolidado"
        f"{f' o {label}' if label else ''} sin decir controlante, la cifra es {consolidado}. "
        f"{controlante} es la fila de al lado (controlante).{extra}"
    )
    keywords = [
        label,
        "consolidado",
        "controlante",
        "RESULTADO NETO",
        consolidado,
        controlante,
        cierre,
    ]
    keywords = [k for k in keywords if k]
    questions = [
        f"Cuál es el RESULTADO NETO DEL PERÍODO al {cierre}",
        f"Resultado atribuible a la participación controlante al {cierre}",
        f"Síntesis de la estructura de resultados consolidada al {cierre}",
    ]
    if label:
        questions.append(f"Cuál es el resultado neto del {label}")
    if len(compare_labels) >= 2:
        questions.append(
            "Compará el resultado neto consolidado de " + " y ".join(compare_labels)
        )
    return content, keywords, questions


def fichas_prompt_lines(rows: list[dict]) -> str:
    if not rows:
        return GRAPH_RULES
    lines = [GRAPH_RULES, "Fichas de este corpus:"]
    for row in rows:
        consolidado = format_ars(row["consolidado"])
        controlante = format_ars(row["controlante"])
        label = row.get("label") or row.get("name")
        cierre = row.get("cierre") or row.get("periodo") or ""
        pagina = row.get("pagina") or 4
        lines.append(
            f"- {label}, EEFF al {cierre}, página {pagina}: consolidado {consolidado}; "
            f"controlante {controlante}."
        )
    if len(rows) >= 2:
        cons = " vs ".join(
            f"{row.get('label') or row.get('name')} = {format_ars(row['consolidado'])}"
            for row in rows
        )
        lines.append(f"Comparación consolidado: {cons}.")
    return "\n".join(lines)


def upsert_graph_prompt(system: str, block: str) -> str:
    wrapped = f"{GRAPH_START}\n{block}\n{GRAPH_END}"
    text = system or ""
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
