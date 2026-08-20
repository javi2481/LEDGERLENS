"""pdftotext helper. Argv list only — never shell=True."""

from __future__ import annotations

import subprocess
from pathlib import Path


class PdfTextError(RuntimeError):
    pass


def pdftotext_argv(pdf: Path, page: int) -> list[str]:
    if page < 1:
        raise PdfTextError("page must be >= 1")
    return [
        "pdftotext",
        "-layout",
        "-f",
        str(int(page)),
        "-l",
        str(int(page)),
        str(pdf),
        "-",
    ]


def pdf_page_text(pdf: Path, page: int, timeout: int = 30) -> str:
    cmd = pdftotext_argv(pdf, page)
    try:
        proc = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError as exc:
        raise PdfTextError("pdftotext not found (install poppler-utils)") from exc
    except subprocess.TimeoutExpired as exc:
        raise PdfTextError(f"pdftotext timed out on {pdf.name}") from exc
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()[:300]
        raise PdfTextError(f"pdftotext failed ({proc.returncode}): {err}")
    return proc.stdout or ""
