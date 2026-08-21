"""Optional RAGFlow HTTP helpers for the retrieval pilot. Not identity."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_NO_RAGFLOW = "no_ragflow"
DEFAULT_API = "http://127.0.0.1/api/v1"


def load_env(path: Path | None = None) -> None:
    env_path = path or (ROOT / ".env")
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def api_base() -> str:
    return os.environ.get("RAGFLOW_URL", DEFAULT_API).rstrip("/")


def ragflow_reachable(timeout: float = 2.0) -> bool:
    """True if something HTTP-speaks at RAGFLOW_URL (even 401)."""
    url = f"{api_base()}/datasets?page_size=1"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except urllib.error.HTTPError:
        return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def api(method: str, path: str, token: str, data: bytes | None = None, timeout: float = 60.0) -> dict:
    req = urllib.request.Request(
        f"{api_base()}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}"},
    )
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def rows_of(payload: dict, *keys: str) -> list:
    data = payload.get("data") or []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            if isinstance(data.get(key), list):
                return data[key]
    return []


def chunk_to_hit(chunk: dict) -> dict | None:
    name = (
        chunk.get("document_keyword")
        or chunk.get("docnm_kwd")
        or chunk.get("doc_name")
        or chunk.get("document_name")
        or ""
    )
    name = str(name)
    page: int | None = None
    for key in ("page_num", "page", "layout_page"):
        raw = chunk.get(key)
        if isinstance(raw, int):
            page = raw
            break
        if isinstance(raw, str) and raw.isdigit():
            page = int(raw)
            break
    positions = chunk.get("positions") or chunk.get("position_int")
    if page is None and isinstance(positions, list) and positions:
        first = positions[0]
        if isinstance(first, (list, tuple)) and first:
            try:
                page = int(first[0])
            except (TypeError, ValueError):
                page = None
        elif isinstance(first, int):
            page = first
    if not name:
        return None
    return {"doc": name, "page": page if page is not None else 1}
