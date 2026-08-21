"""Parse cover → recipe. Filename is not the porter."""

from __future__ import annotations

from pathlib import Path

from schemas.classify import UNKNOWN, classify_pdf, classify_text
from schemas.corpus import SAMPLES

PDF_1T26 = SAMPLES / "BYMA_-_EEFF_31-03-2026_VF.pdf"
PDF_COMUNICADO = SAMPLES / "BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf"
PDF_MEMORIA_FILE = SAMPLES / "BYMA-MEMORIA_2024_y_EEFF_31-12-2024.pdf"
PDF_DECK = SAMPLES / "Presentacion_de_resultados_BYMA-2T26.pdf"
PDF_TRANSCRIPT = SAMPLES / "BYMA_2T26_Transcripcion_Resultados_ES.pdf"


def test_cover_eeff_is_financial_statement() -> None:
    assert classify_text("Estados Financieros Condensados Intermedios Consolidados") == "financial_statement"
    assert classify_pdf(PDF_1T26) == "financial_statement"


def test_cover_comunicado_is_press_release() -> None:
    assert classify_text("BYMA anuncia resultados para el 1T26. El presente comunicado de prensa") == "press_release"
    assert classify_pdf(PDF_COMUNICADO) == "press_release"


def test_cover_memoria_is_unknown() -> None:
    assert classify_text("MEMORIA Y ESTADOS CONTABLES 2024\nEstados financieros") == UNKNOWN
    assert classify_pdf(PDF_MEMORIA_FILE) == UNKNOWN
    assert classify_pdf(SAMPLES / "BYMA-MEMORIA_2025.pdf") == UNKNOWN


def test_cover_deck_and_transcript_are_unknown() -> None:
    assert classify_text("Presentación de Resultados 2° TRIMESTRE 2026") == UNKNOWN
    assert classify_pdf(PDF_DECK) == UNKNOWN
    assert classify_pdf(PDF_TRANSCRIPT) == UNKNOWN


def test_missing_artifact_is_unknown(tmp_path: Path) -> None:
    pdf = tmp_path / "scan_8841.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    assert classify_pdf(pdf) == UNKNOWN
