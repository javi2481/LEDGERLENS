"""Extract typed claims from a directory of PDFs. No RAGFlow."""

from __future__ import annotations

from pathlib import Path

from schemas.claim import Claim, claims_from_financial_statement
from schemas.extract import extract_financial_statement
from schemas.finance_lines import claims_from_pnl_lines
from schemas.parse_artifact import load_parse, page_text
from schemas.press_release import claims_from_press_release, extract_press_release

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "docs" / "archivos_muestra"


def extract_claims_from_dir(directory: Path | None = None) -> tuple[Claim, ...]:
    folder = directory or SAMPLES
    out: list[Claim] = []
    for pdf in sorted(folder.glob("*.pdf")):
        row = extract_financial_statement(pdf)
        if row is not None:
            out.extend(claims_from_financial_statement(row))
            if row.source_page:
                artifact = load_parse(pdf)
                if artifact is not None:
                    text = page_text(artifact, row.source_page)
                    out.extend(claims_from_pnl_lines(text, row))
            continue
        press = extract_press_release(pdf)
        if press is not None:
            out.extend(claims_from_press_release(press))
    return tuple(out)
