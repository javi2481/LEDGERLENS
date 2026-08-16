#!/usr/bin/env python3
"""One-PDF Graph overlay. Not used by scripts/up.sh. Does not touch demo_4 or MinerU."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_1T26 = ROOT / "docs" / "archivos_muestra" / "BYMA_-_EEFF_31-03-2026_VF.pdf"
OUTPUT_DIR = ROOT / "outputs" / "graph-1t26"
DOCLING_JSON = OUTPUT_DIR / "docling-document.json"
RANGE_STAMP = OUTPUT_DIR / "page-range.txt"
# Full 81-page TableFormer OOMs (~page 51). Both gold P&L rows sit on page 4.
PAGE_RANGE = (4, 4)
GOLD = {
    "consolidado": "21262335",
    "controlante": "21259769",
}
# Chat demo stays llama-3.3-70b-versatile (100k TPD / 12k TPM, exhausted today).
# 8b free TPM is 6k and Graph's schema+page is ~7k tokens. gpt-oss-120b is 8k TPM / 200k TPD.
DEFAULT_MODEL = "openai/gpt-oss-120b"


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
    print(f"converting {pdf.name} (ocr=off, pages={PAGE_RANGE[0]}-{PAGE_RANGE[1]})...")
    result = converter.convert(str(pdf), page_range=PAGE_RANGE)
    dest.parent.mkdir(parents=True, exist_ok=True)
    result.document.save_as_json(dest)
    RANGE_STAMP.write_text(f"{PAGE_RANGE[0]}-{PAGE_RANGE[1]}\n", encoding="utf-8")
    print(f"wrote {dest}")
    return dest


def _digits(value: object) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def gold_report(graph: object) -> int:
    """Return 0 only if two distinct nodes hold the gold amounts."""
    consolidado_ids: list[str] = []
    controlante_ids: list[str] = []
    if graph is None:
        print("gold FAIL: no graph")
        return 1
    for node_id, data in graph.nodes(data=True):
        blob = json.dumps(data, default=str)
        digits = _digits(blob)
        labels = blob.lower()
        if GOLD["consolidado"] in digits or GOLD["consolidado"] in blob:
            consolidado_ids.append(str(node_id))
            print(f"gold hit consolidado node={node_id} page={data.get('fuente_pagina') or data.get('__provenance__')}")
        if GOLD["controlante"] in digits or GOLD["controlante"] in blob:
            controlante_ids.append(str(node_id))
            print(f"gold hit controlante node={node_id} page={data.get('fuente_pagina') or data.get('__provenance__')}")
        if "consolidado" in labels or "controlante" in labels:
            print(f"node={node_id} keys={sorted(data.keys())}")
    c_set, t_set = set(consolidado_ids), set(controlante_ids)
    if c_set and t_set and c_set.isdisjoint(t_set):
        print("gold PASS: two distinct nodes")
        return 0
    print(
        "gold FAIL: "
        f"consolidado_nodes={consolidado_ids} controlante_nodes={controlante_ids}"
    )
    return 2


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
    from docling_graph.config import LlmRuntimeOverrides

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    wanted = f"{PAGE_RANGE[0]}-{PAGE_RANGE[1]}"
    have = RANGE_STAMP.read_text(encoding="utf-8").strip() if RANGE_STAMP.is_file() else ""
    if have != wanted and DOCLING_JSON.is_file():
        DOCLING_JSON.unlink()
    if not DOCLING_JSON.is_file():
        convert_pdf_without_ocr(PDF_1T26, DOCLING_JSON)

    model = os.environ.get("GRAPH_GROQ_MODEL", DEFAULT_MODEL)
    print(f"graph model={model} contract=direct pages={wanted}")
    config = PipelineConfig(
        source=str(DOCLING_JSON),
        template="templates.EeffByma",
        backend="llm",
        inference="remote",
        processing_mode="many-to-one",
        extraction_contract="direct",
        llm_input_format="markdown",
        gleaning_enabled=False,
        parallel_workers=1,
        provenance="standard",
        provider_override="groq",
        model_override=model,
        llm_overrides=LlmRuntimeOverrides(max_output_tokens=4096),
        docling_config="ocr",
        output_dir=str(OUTPUT_DIR),
    )
    context = run_pipeline(config)
    graph = getattr(context, "knowledge_graph", None)
    n_nodes = graph.number_of_nodes() if graph is not None else 0
    print(f"nodes={n_nodes} output={OUTPUT_DIR}")
    print(f"gold consolidado={GOLD['consolidado']} controlante={GOLD['controlante']}")
    return gold_report(graph)


if __name__ == "__main__":
    raise SystemExit(main())
