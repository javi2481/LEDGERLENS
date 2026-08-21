"""Optional cover-page orientation. Skip without Paddle. Not identity OCR."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from schemas.corpus import SAMPLES

SKIP_NO_PADDLE = "no_paddle"
SKIP_NO_PDFTOPPM = "no_pdftoppm"
MODEL_ID = "PP-LCNet_x1_0_doc_ori"


def paddle_available() -> bool:
    try:
        import paddlex  # noqa: F401

        return True
    except ImportError:
        return False


def pdftoppm_cmd(pdf: Path, dest_prefix: Path) -> list[str]:
    """Argv list only. Never interpolate into a shell string."""
    return ["pdftoppm", "-f", "1", "-l", "1", "-png", str(pdf), str(dest_prefix)]


def _render_cover(pdf: Path, work: Path) -> Path | None:
    if shutil.which("pdftoppm") is None:
        return None
    prefix = work / "cover"
    subprocess.run(pdftoppm_cmd(pdf, prefix), check=True, capture_output=True, shell=False)
    pngs = sorted(work.glob("cover*.png"))
    return pngs[0] if pngs else None


def _predict_angle(image: Path) -> str | None:
    from paddlex import create_model

    model = create_model(MODEL_ID)
    results = list(model.predict(str(image)))
    if not results:
        return None
    row = results[0]
    if isinstance(row, dict):
        label = row.get("label") or row.get("class_ids") or row.get("angle")
        return str(label)
    for attr in ("label", "angle", "class_ids"):
        if hasattr(row, attr):
            return str(getattr(row, attr))
    return str(row)


def probe_directory(directory: Path | None = None) -> dict:
    folder = (directory or SAMPLES).resolve()
    if not paddle_available():
        return {"skipped": True, "reason": SKIP_NO_PADDLE, "rows": []}
    if shutil.which("pdftoppm") is None:
        return {"skipped": True, "reason": SKIP_NO_PDFTOPPM, "rows": []}
    rows: list[dict] = []
    for pdf in sorted(folder.glob("*.pdf")):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            try:
                cover = _render_cover(pdf, work)
                if cover is None:
                    rows.append({"name": pdf.name, "angle": None, "reason": "no_cover"})
                    continue
                angle = _predict_angle(cover)
                rows.append({"name": pdf.name, "angle": angle, "reason": None})
            except Exception as exc:  # probe must not fail CI
                rows.append({"name": pdf.name, "angle": None, "reason": str(exc)})
    return {"skipped": False, "reason": None, "rows": rows}


def report_json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
