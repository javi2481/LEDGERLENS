"""Academic HTML dossier from accepted claims + gold evals. No RAGFlow."""

from __future__ import annotations

import json
from pathlib import Path

from schemas.claim import Claim
from schemas.review import Verdict, flagged, publishable, rejected, verdict_for

ROOT = Path(__file__).resolve().parents[1]
EVAL_FILES = (
    ROOT / "evals" / "identity_v1.json",
    ROOT / "evals" / "identity_v2.json",
    ROOT / "evals" / "press_v1.json",
    ROOT / "evals" / "presentation_v1.json",
)


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_eval_cases() -> list[dict]:
    cases: list[dict] = []
    for path in EVAL_FILES:
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload.get("cases") or ():
            if isinstance(row, dict):
                cases.append(row)
    return cases


def identity_qa_rows(
    cases: list[dict],
    published: tuple[Claim, ...] | list[Claim],
) -> list[dict]:
    by_key = {c.identity_key: c for c in published}
    rows: list[dict] = []
    for case in cases:
        if case.get("route") != "identity" or case.get("skip"):
            continue
        key = case.get("expected_identity")
        if not isinstance(key, str) or key not in by_key:
            continue
        claim = by_key[key]
        rows.append(
            {
                "id": case.get("id"),
                "question": case.get("question") or "",
                "value": claim.value,
                "identity_key": key,
                "page": claim.source_page,
                "source_text": claim.source_text or "",
            }
        )
    return rows


def abstain_rows(cases: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for case in cases:
        if case.get("route") != "abstain":
            continue
        rows.append(
            {
                "id": case.get("id"),
                "question": case.get("question") or "",
                "reason": case.get("expected_abstain"),
            }
        )
    return rows


def render_dossier(
    claims: tuple[Claim, ...] | list[Claim],
    *,
    verdicts: dict[str, Verdict] | None = None,
    cases: list[dict] | None = None,
    classified: dict[str, str] | None = None,
) -> str:
    table = verdicts or {}
    published = publishable(claims, table)
    flags = flagged(claims, table)
    rejects = rejected(claims, table)
    gold = cases if cases is not None else load_eval_cases()
    qa = identity_qa_rows(gold, published)
    abs_rows = abstain_rows(gold)

    fact_rows = []
    for claim in published:
        page = "" if claim.source_page is None else str(claim.source_page)
        fact_rows.append(
            "<tr>"
            f"<td>{_esc(claim.period)}</td>"
            f"<td>{_esc(claim.identity_key)}</td>"
            f"<td>{_esc(claim.value)}</td>"
            f"<td>{_esc(page)}</td>"
            f"<td>{_esc(claim.source_text or '')}</td>"
            "</tr>"
        )
    qa_html = []
    for row in qa:
        page = "" if row["page"] is None else str(row["page"])
        qa_html.append(
            "<tr>"
            f"<td>{_esc(str(row['id'] or ''))}</td>"
            f"<td>{_esc(row['question'])}</td>"
            f"<td>{_esc(str(row['value']))}</td>"
            f"<td>{_esc(str(row['identity_key']))}</td>"
            f"<td>{_esc(page)}</td>"
            f"<td>{_esc(str(row['source_text']))}</td>"
            "</tr>"
        )
    abs_html = []
    for row in abs_rows:
        abs_html.append(
            "<tr>"
            f"<td>{_esc(str(row['id'] or ''))}</td>"
            f"<td>{_esc(row['question'])}</td>"
            "<td>abstain</td>"
            "</tr>"
        )
    annex = []
    for claim in list(flags) + list(rejects):
        annex.append(
            "<tr>"
            f"<td>{_esc(claim.identity_key)}</td>"
            f"<td>{_esc(verdict_for(claim.identity_key, table))}</td>"
            f"<td>{_esc(claim.value)}</td>"
            "</tr>"
        )
    class_rows = []
    for name, recipe in sorted((classified or {}).items()):
        class_rows.append(f"<tr><td>{_esc(name)}</td><td>{_esc(recipe)}</td></tr>")

    css = (
        "body{font-family:sans-serif;margin:24px;max-width:1100px}"
        "table{border-collapse:collapse;width:100%;margin-bottom:24px}"
        "th,td{border:1px solid #ccc;padding:6px;text-align:left;font-size:13px}"
        "th{background:#f4f4f4}h1,h2{margin-top:28px}"
    )
    return (
        "<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>"
        "<title>Dossier Claimprint BYMA</title>"
        f"<style>{css}</style></head><body>"
        "<h1>Dossier de hechos BYMA</h1>"
        "<p>Cifras del IDP (claims aceptados). El chat RAGFlow no es la fuente de verdad. "
        "Citas = <code>source_text</code> del claim, no un índice inventado.</p>"
        "<h2>Clasificación del corpus</h2>"
        "<table><thead><tr><th>PDF</th><th>receta</th></tr></thead><tbody>"
        f"{''.join(class_rows) or '<tr><td colspan=2>Sin clasificar</td></tr>'}"
        "</tbody></table>"
        "<h2 id='hechos'>Hechos publicados</h2>"
        "<table><thead><tr><th>período</th><th>identity_key</th><th>valor</th>"
        "<th>página</th><th>source_text</th></tr></thead><tbody>"
        f"{''.join(fact_rows) or '<tr><td colspan=5>Sin hechos</td></tr>'}"
        "</tbody></table>"
        "<h2>Preguntas y respuestas (evals identity)</h2>"
        "<table><thead><tr><th>id</th><th>pregunta</th><th>valor</th>"
        "<th>identity_key</th><th>página</th><th>source_text</th></tr></thead><tbody>"
        f"{''.join(qa_html)}</tbody></table>"
        "<h2>Abstenciones</h2>"
        "<p>El sistema se calla; no inventa el número.</p>"
        "<table><thead><tr><th>id</th><th>pregunta</th><th>ruta</th></tr></thead><tbody>"
        f"{''.join(abs_html)}</tbody></table>"
        "<h2>Anexo HITL</h2>"
        "<table><thead><tr><th>identity_key</th><th>veredicto</th><th>valor</th></tr></thead><tbody>"
        f"{''.join(annex) or '<tr><td colspan=3>Sin reject/flag (todo accept)</td></tr>'}"
        "</tbody></table></body></html>"
    )
