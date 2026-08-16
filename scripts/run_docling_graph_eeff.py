#!/usr/bin/env python3
"""One-PDF Graph overlay. Not used by scripts/up.sh. Does not touch demo_4 or MinerU."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_1T26 = ROOT / "docs" / "archivos_muestra" / "BYMA_-_EEFF_31-03-2026_VF.pdf"
OUTPUT_DIR = ROOT / "outputs" / "graph-1t26"
DOCLING_JSON = OUTPUT_DIR / "docling-document.json"
GOLD = {
    "consolidado": "21262335",
    "controlante": "21259769",
}


def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def convert_pdf_without_ocr(pdf: Path, dest: Path) -> Path:
    """Digital EEFF: layout + tables, no OCR. Graph's default OCR path crashes RapidOCR/torch here."""
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption

    opts = PdfPipelineOptions()
    opts.do_ocr = False
    opts.do_table_structure = True
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
    )
    print(f"converting {pdf.name} (ocr=off)...")
    result = converter.convert(str(pdf))
    dest.parent.mkdir(parents=True, exist_ok=True)
    result.document.save_as_json(dest)
    print(f"wrote {dest}")
    return dest


def main() -> int:
    sys.path.insert(0, str(ROOT))
    load_env(ROOT / ".env")
    if not os.environ.get("GROQ_API_KEY"):
        print("error: GROQ_API_KEY missing in env / .env", file=sys.stderr)
        return 1
    if not PDF_1T26.is_file():
        print(f"error: missing {PDF_1T26}", file=sys.stderr)
        return 1

    from docling_graph import PipelineConfig, run_pipeline

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not DOCLING_JSON.is_file():
        convert_pdf_without_ocr(PDF_1T26, DOCLING_JSON)
    config = PipelineConfig(
        source=str(DOCLING_JSON),
        template="templates.EeffByma",
        backend="llm",
        inference="remote",
        processing_mode="many-to-one",
        extraction_contract="dense",
        provenance="standard",
        provider_override="groq",
        model_override="llama-3.3-70b-versatile",
        docling_config="ocr",
        output_dir=str(OUTPUT_DIR),
    )
    context = run_pipeline(config)
    graph = getattr(context, "knowledge_graph", None)
    n_nodes = graph.number_of_nodes() if graph is not None else 0
    print(f"nodes={n_nodes} output={OUTPUT_DIR}")
    print(f"gold consolidado={GOLD['consolidado']} controlante={GOLD['controlante']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
