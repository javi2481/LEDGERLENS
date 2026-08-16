#!/usr/bin/env python3
"""EEFF Graph overlay for any dedicated filing. Not used by scripts/up.sh. Does not touch MinerU."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "docs" / "archivos_muestra"
PDF_1T26 = SAMPLES / "BYMA_-_EEFF_31-03-2026_VF.pdf"
PDF_2T26 = SAMPLES / "BYMA - EEFF 30-06-2026.pdf"
sys.path.insert(0, str(ROOT / "scripts"))
from graph_hechos import format_ars, needs_graph  # noqa: E402
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
    parser = argparse.ArgumentParser(description="EEFF Graph overlay (any dedicated filing)")
    parser.add_argument("--preset", choices=["1t26", "2t26"], default=None)
    parser.add_argument("--pdf", type=Path, default=None)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Every dedicated EEFF PDF in docs/archivos_muestra (not memorias/comunicados)",
    )
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
    elif args.preset == "1t26" or (args.pdf is None and not args.all):
        args.pdf = args.pdf or PDF_1T26
        args.out = args.out or (ROOT / "outputs" / "graph-1t26")
        args.consolidado = args.consolidado or "21262335"
        args.controlante = args.controlante or "21259769"
    return args


def slug_for(pdf: Path) -> str:
    return pdf.stem.replace(" ", "_").replace(".", "_")[:80]


def ficha_from_graph(graph: object, pdf_name: str, pagina: int, gold: dict[str, str] | None) -> dict:
    row: dict = {"name": pdf_name, "pagina": pagina}
    if gold:
        row["consolidado"] = format_ars(gold["consolidado"])
        row["controlante"] = format_ars(gold["controlante"])
    if graph is None:
        return row
    for _node_id, data in graph.nodes(data=True):
        blob = json.dumps(data, default=str)
        estado = str(data.get("estado") or "")
        monto = data.get("monto")
        valor = monto.get("valor") if isinstance(monto, dict) else None
        periodo = data.get("periodo")
        if periodo and "periodo" not in row:
            row["periodo"] = str(periodo)
        page = data.get("fuente_pagina")
        if page is not None:
            row["pagina"] = page
        if gold or not valor:
            continue
        if ("consolidado" in estado or "resultado_neto" in blob) and "controlante" not in estado:
            row["consolidado"] = format_ars(str(valor))
        if "controlante" in estado or "atribuible" in blob:
            row["controlante"] = format_ars(str(valor))
    return row


def run_one(pdf: Path, output_dir: Path, page_range: tuple[int, int], gold: dict[str, str] | None) -> int:
    from docling_graph import PipelineConfig, run_pipeline
    from docling_graph.config import LlmRuntimeOverrides

    docling_json = output_dir / "docling-document.json"
    stamp = output_dir / "page-range.txt"
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
    ficha = ficha_from_graph(graph, pdf.name, page_range[0], gold)
    (output_dir / "ficha.json").write_text(
        json.dumps(ficha, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output_dir / 'ficha.json'}")
    if gold:
        print(f"gold consolidado={gold['consolidado']} controlante={gold['controlante']}")
        return gold_report(graph, gold)
    if not ficha.get("consolidado") or not ficha.get("controlante"):
        print("warn: ficha missing consolidado/controlante; push will skip this PDF")
        return 2
    return 0


def main() -> int:
    args = parse_args()
    sys.path.insert(0, str(ROOT))
    load_env(ROOT / ".env")
    if not os.environ.get("GROQ_API_KEY"):
        print("error: GROQ_API_KEY missing in env / .env", file=sys.stderr)
        return 1

    page_range = parse_pages(args.pages)
    jobs: list[tuple[Path, Path, dict[str, str] | None]] = []
    if args.all:
        pdfs = sorted(p for p in SAMPLES.glob("*.pdf") if needs_graph(p.name))
        if not pdfs:
            print(f"error: no dedicated EEFF PDFs in {SAMPLES}", file=sys.stderr)
            return 1
        for pdf in pdfs:
            gold = None
            if pdf.resolve() == PDF_1T26.resolve():
                gold = {"consolidado": "21262335", "controlante": "21259769"}
            elif pdf.resolve() == PDF_2T26.resolve():
                gold = {"consolidado": "81956525", "controlante": "81946993"}
            jobs.append((pdf, ROOT / "outputs" / f"graph-{slug_for(pdf)}", gold))
    else:
        pdf = args.pdf if args.pdf.is_absolute() else ROOT / args.pdf
        if not pdf.is_file():
            print(f"error: missing {pdf}", file=sys.stderr)
            return 1
        out = args.out or (ROOT / "outputs" / f"graph-{slug_for(pdf)}")
        output_dir = out if out.is_absolute() else ROOT / out
        gold = None
        if args.consolidado and args.controlante:
            gold = {"consolidado": args.consolidado, "controlante": args.controlante}
        jobs.append((pdf, output_dir, gold))

    worst = 0
    for pdf, output_dir, gold in jobs:
        code = run_one(pdf, output_dir, page_range, gold)
        worst = max(worst, code)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
