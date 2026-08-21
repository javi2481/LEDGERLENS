"""MinerU artifacts: flatten tables, no pdftotext fallback."""

from __future__ import annotations

from pathlib import Path

from schemas.extract import extract_financial_statement
from schemas.parse_artifact import flatten_mineru, load_parse, split_pages


def test_flatten_markdown_table_keeps_label_and_amount() -> None:
    raw = "| RESULTADO NETO DEL PERÍODO | 21.262.335 | 22.362.983 |"
    flat = flatten_mineru(raw)
    assert "RESULTADO NETO DEL PERÍODO" in flat
    assert "21.262.335" in flat


def test_split_page_markers() -> None:
    raw = "<!-- page: 1 -->\ncover\n<!-- page: 4 -->\nRESULTADO NETO\n"
    pages = dict(split_pages(raw))
    assert pages[1] == "cover"
    assert "RESULTADO NETO" in pages[4]


def test_missing_parse_does_not_extract(tmp_path: Path) -> None:
    pdf = tmp_path / "scan_8841.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    assert load_parse(pdf) is None
    assert extract_financial_statement(pdf) is None
