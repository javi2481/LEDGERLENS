# Parser Naive (fallback)

No es pesado: **salta** OCR/TSR/DLR. Más liviano y más rápido que DeepDoc. Los PDFs con capa de texto (`pdftotext`) alcanzan. [Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser).

Default del demo: **Docling** clásico ([nota](docling-serve.md)). Naive si el sidecar no está. DeepDoc si el PDF es escaneo.

## Quick path (UI)

1. Dataset → PDF parser = **Naive** solo si Docling Serve no corre.
2. Preferir Docling para EEFF / tablas.

## Details

| Tema | Decisión |
|------|----------|
| Default | Docling Serve CPU |
| Fallback | Naive (texto); DeepDoc (escaneo) |
| Extra | PaddleOCR (profile), no MinerU |
| Dump | `research/extract-ragflow-select-pdf-parser.json` |

## Checklist

- [x] `pdftotext` / `./scripts/check.sh`
- [x] E2E in-corpus Windows 32 GB con Naive (Q3 consolidado 21.262.335, comunicado 8 may 2026) — histórico
- [x] Empty response / Show Quote (KB vacía vs evidencia)

## Next step

No reabrir Naive como default. Re-parse con Docling.
