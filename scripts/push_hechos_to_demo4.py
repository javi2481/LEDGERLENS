#!/usr/bin/env python3
"""Upload Graph EEFF facts into demo_4 and point chat_demo_4 at them.

Does not reparse the BYMA PDFs. Parses only docs/hechos_eeff.md (Naive).
Not called by scripts/up.sh.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
HECHOS = ROOT / "docs" / "hechos_eeff.md"
API = os.environ.get("RAGFLOW_URL", "http://127.0.0.1/api/v1").rstrip("/")
DATASET = "demo_4"
CHAT = "chat_demo_4"
DOC_NAME = "hechos_eeff.md"

GRAPH_PROMPT = (
    "Responde solo en español. Cita los fragmentos. Si no hay evidencia, usa la respuesta vacía. "
    "No inventes cifras.\n"
    "Si el conocimiento incluye fichas EEFF (Docling Graph), esas cifras tienen prioridad "
    "sobre otras filas de la misma tabla del PDF. Distinguí consolidado "
    "(RESULTADO NETO DEL PERÍODO del estado consolidado) vs controlante "
    "(atribuible a la participación controlante). No uses la columna del ejercicio anterior. "
    "Si preguntan 1T26 y 2T26, usá ambas fichas y citá página.\n"
    "Eres un asistente inteligente. Resume el contenido de la base de conocimiento para "
    "responder la pregunta. Enumera los datos de la base de conocimiento y responde con detalle. "
    "Cuando todo el contenido de la base de conocimiento sea irrelevante para la pregunta, "
    'tu respuesta debe incluir la frase "No hay evidencia suficiente en los documentos '
    'indexados para responder. No invento datos.". Las respuestas necesitan considerar el '
    "historial de chat.\n"
    "Aquí está la base de conocimiento:\n{knowledge}\n"
    "Esa es la base de conocimiento."
)


def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def token_from_mysql() -> str:
    cmd = (
        'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N rag_flow '
        '-e "SELECT token FROM api_token LIMIT 1;"'
    )
    out = subprocess.check_output(
        ["docker", "exec", "ledgerlens-mysql-1", "sh", "-c", cmd],
        stderr=subprocess.DEVNULL,
    )
    token = out.decode("utf-8", errors="replace").strip().splitlines()[-1].strip()
    if not token:
        raise SystemExit("error: no api_token in rag_flow")
    return token


def api(method: str, path: str, token: str, data: bytes | None = None, content_type: str | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}"},
    )
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"error: {method} {path} -> {exc.code} {body[:500]}") from exc


def multipart(field: str, filename: str, blob: bytes) -> tuple[bytes, str]:
    boundary = "----ledgerlenshechos"
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'.encode(),
        b"Content-Type: text/markdown\r\n\r\n",
        blob,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def main() -> int:
    load_env(ROOT / ".env")
    if not HECHOS.is_file():
        print(f"error: missing {HECHOS}", file=sys.stderr)
        return 1
    token = os.environ.get("RAGFLOW_API_KEY") or token_from_mysql()

    datasets = api("GET", f"/datasets?name={DATASET}", token)
    rows = datasets.get("data") or []
    if isinstance(rows, dict):
        rows = rows.get("datasets") or rows.get("kbs") or []
    ds = next((r for r in rows if r.get("name") == DATASET), None)
    if not ds:
        print("error: dataset demo_4 not found via API", file=sys.stderr)
        return 1
    ds_id = ds["id"]

    docs = api("GET", f"/datasets/{ds_id}/documents?page_size=100", token)
    doc_rows = docs.get("data") or {}
    if isinstance(doc_rows, dict):
        doc_rows = doc_rows.get("docs") or doc_rows.get("documents") or []
    existing = next((d for d in doc_rows if d.get("name") == DOC_NAME), None)
    if existing:
        api(
            "DELETE",
            f"/datasets/{ds_id}/documents",
            token,
            json.dumps({"ids": [existing["id"]]}).encode(),
            "application/json",
        )

    body, ctype = multipart("file", DOC_NAME, HECHOS.read_bytes())
    uploaded = api("POST", f"/datasets/{ds_id}/documents", token, body, ctype)
    created = uploaded.get("data") or []
    if isinstance(created, dict):
        created = created.get("docs") or created.get("documents") or [created]
    doc_id = created[0]["id"]
    api(
        "PUT",
        f"/datasets/{ds_id}/documents/{doc_id}",
        token,
        json.dumps({"chunk_method": "manual"}).encode(),
        "application/json",
    )
    text = HECHOS.read_text(encoding="utf-8")
    keywords = [
        "1T26",
        "2T26",
        "consolidado",
        "controlante",
        "RESULTADO NETO",
        "21.262.335",
        "21.259.769",
        "81.956.525",
        "81.946.993",
    ]
    added = api(
        "POST",
        f"/datasets/{ds_id}/documents/{doc_id}/chunks",
        token,
        json.dumps(
            {
                "content": text,
                "important_keywords": keywords,
                "questions": [
                    "Cuál es el RESULTADO NETO DEL PERÍODO de BYMA al 31 de marzo de 2026",
                    "Resultado atribuible a la participación controlante al 31 de marzo de 2026",
                    "Síntesis de la estructura de resultados consolidada al 31 de marzo de 2026",
                    "Cuál es el resultado neto del 2T26",
                    "Resultado neto consolidado del EEFF al 30 de junio de 2026",
                    "Resultado atribuible a los propietarios de la controlante al 30 de junio de 2026",
                    "Compará el resultado neto consolidado de 2T26 y 1T26",
                ],
            }
        ).encode(),
        "application/json",
    )
    if added.get("code") not in (0, None):
        print(f"error: add chunk {added}", file=sys.stderr)
        return 1
    print("ok: injected Graph hechos as a manual chunk (PDFs untouched)")

    chats = api("GET", f"/chats?name={CHAT}", token)
    chat_rows = chats.get("data") or {}
    if isinstance(chat_rows, dict):
        chat_rows = chat_rows.get("chats") or []
    chat = next((c for c in chat_rows if c.get("name") == CHAT), None)
    if not chat:
        print("error: chat_demo_4 not found", file=sys.stderr)
        return 1
    prompt = dict(chat.get("prompt_config") or {})
    prompt["system"] = GRAPH_PROMPT
    prompt["quote"] = True
    api(
        "PUT",
        f"/chats/{chat['id']}",
        token,
        json.dumps({"prompt_config": prompt}).encode(),
        "application/json",
    )
    print(f"ok: {DOC_NAME} in {DATASET}; prompt updated on {CHAT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
