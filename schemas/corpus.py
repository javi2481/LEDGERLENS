"""Extract typed claims from a directory of PDFs. No RAGFlow."""

from __future__ import annotations

from pathlib import Path

from schemas.claim import Claim, claims_from_financial_statement
from schemas.extract import extract_financial_statement
from schemas.finance_lines import claims_from_pnl_lines
from schemas.page_text import pdf_page_text

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "docs" / "archivos_muestra"


def extract_claims_from_dir(directory: Path | None = None) -> tuple[Claim, ...]:
    folder = directory or SAMPLES
    out: list[Claim] = []
    for pdf in sorted(folder.glob("*.pdf")):
        row = extract_financial_statement(pdf)
        if row is None:
            continue
        out.extend(claims_from_financial_statement(row))
        if row.source_page:
            text = pdf_page_text(pdf, row.source_page)
            out.extend(claims_from_pnl_lines(text, row))
    return tuple(out)
