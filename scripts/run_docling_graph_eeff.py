#!/usr/bin/env python3
"""One-PDF Graph overlay. Not used by scripts/up.sh. Does not touch demo_4 or MinerU."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_1T26 = ROOT / "docs" / "archivos_muestra" / "BYMA_-_EEFF_31-03-2026_VF.pdf"
PDF_2T26 = ROOT / "docs" / "archivos_muestra" / "BYMA - EEFF 30-06-2026.pdf"
# Chat demo stays llama-3.3-70b-versatile. Overlay uses gpt-oss-120b (8k TPM / 200k TPD).
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


def convert_pdf_without_ocr(pdf: Path, dest: Path, page_range: tuple[int, int], stamp: Path) -> Path:
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
    print(f"converting {pdf.name} (ocr=off, pages={page_range[0]}-{page_range[1]})...")
    result = converter.convert(str(pdf), page_range=page_range)
    dest.parent.mkdir(parents=True, exist_ok=True)
    result.document.save_as_json(dest)
    stamp.write_text(f"{page_range[0]}-{page_range[1]}\n", encoding="utf-8")
    print(f"wrote {dest}")
    return dest


def _digits(value: object) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def gold_report(graph: object, gold: dict[str, str]) -> int:
    """Return 0 only if two distinct nodes hold the gold amounts."""
    consolidado_ids: list[str] = []
    controlante_ids: list[str] = []
    if graph is None:
        print("gold FAIL: no graph")
        return 1
    for node_id, data in graph.nodes(data=True):
        blob = json.dumps(data, default=str)
        digits = _digits(blob)
        print(f"node={node_id} payload={blob[:1200]}")
        if gold["consolidado"] in digits or gold["consolidado"] in blob:
            consolidado_ids.append(str(node_id))
            print(f"gold hit consolidado node={node_id} page={data.get('fuente_pagina') or data.get('__provenance__')}")
        if gold["controlante"] in digits or gold["controlante"] in blob:
            controlante_ids.append(str(node_id))
            print(f"gold hit controlante node={node_id} page={data.get('fuente_pagina') or data.get('__provenance__')}")
    c_set, t_set = set(consolidado_ids), set(controlante_ids)
    if c_set and t_set and c_set.isdisjoint(t_set):
        print("gold PASS: two distinct nodes")
        return 0
    print(
        "gold FAIL: "
        f"consolidado_nodes={consolidado_ids} controlante_nodes={controlante_ids}"
    )
    return 2


def parse_pages(text: str) -> tuple[int, int]:
    start, end = text.split("-", 1)
    return int(start), int(end)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experimental EEFF Graph overlay")
    parser.add_argument("--preset", choices=["1t26", "2t26"], default=None)
    parser.add_argument("--pdf", type=Path, default=None)
    parser.add_argument("--pages", default="4-4")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--consolidado", default=None)
    parser.add_argument("--controlante", default=None)
    args = parser.parse_args()
    if args.preset == "2t26":
        args.pdf = args.pdf or PDF_2T26
        args.out = args.out or (ROOT / "outputs" / "graph-2t26")
        args.consolidado = args.consolidado or "81956525"
        args.controlante = args.controlante or "81946993"
    else:
        args.pdf = args.pdf or PDF_1T26
        args.out = args.out or (ROOT / "outputs" / "graph-1t26")
        args.consolidado = args.consolidado or "21262335"
        args.controlante = args.controlante or "21259769"
    return args


def main() -> int:
    args = parse_args()
    sys.path.insert(0, str(ROOT))
    load_env(ROOT / ".env")
    if not os.environ.get("GROQ_API_KEY"):
        print("error: GROQ_API_KEY missing in env / .env", file=sys.stderr)
        return 1
    pdf = args.pdf if args.pdf.is_absolute() else ROOT / args.pdf
    if not pdf.is_file():
        print(f"error: missing {pdf}", file=sys.stderr)
        return 1

    from docling_graph import PipelineConfig, run_pipeline
    from docling_graph.config import LlmRuntimeOverrides

    page_range = parse_pages(args.pages)
    output_dir = args.out if args.out.is_absolute() else ROOT / args.out
    docling_json = output_dir / "docling-document.json"
    stamp = output_dir / "page-range.txt"
    gold = {"consolidado": args.consolidado, "controlante": args.controlante}

    output_dir.mkdir(parents=True, exist_ok=True)
    wanted = f"{page_range[0]}-{page_range[1]}"
    have = stamp.read_text(encoding="utf-8").strip() if stamp.is_file() else ""
    if have != wanted and docling_json.is_file():
        docling_json.unlink()
    if not docling_json.is_file():
        convert_pdf_without_ocr(pdf, docling_json, page_range, stamp)

    model = os.environ.get("GRAPH_GROQ_MODEL", DEFAULT_MODEL)
    print(f"graph model={model} contract=direct pages={wanted} pdf={pdf.name}")
    config = PipelineConfig(
        source=str(docling_json),
        template="templates.EeffByma",
        backend="llm",
        inference="remote",
        processing_mode="many-to-one",
        extraction_contract="direct",
        llm_input_format="markdown",
        structured_output=False,
        gleaning_enabled=False,
        parallel_workers=1,
        provenance="standard",
        provider_override="groq",
        model_override=model,
        llm_overrides=LlmRuntimeOverrides(max_output_tokens=4096),
        docling_config="ocr",
        output_dir=str(output_dir),
    )
    context = run_pipeline(config)
    graph = getattr(context, "knowledge_graph", None)
    n_nodes = graph.number_of_nodes() if graph is not None else 0
    print(f"nodes={n_nodes} output={output_dir}")
    print(f"gold consolidado={gold['consolidado']} controlante={gold['controlante']}")
    return gold_report(graph, gold)


if __name__ == "__main__":
    raise SystemExit(main())
