# Parser Naive (aplicado)

No es pesado: **salta** OCR/TSR/DLR. Más liviano y más rápido que DeepDoc. Los PDFs de `examples/synthetic/` tienen capa de texto (`pdftotext` los lee enteros). [Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser).

Default del demo: **Naive**. DeepDoc / PaddleOCR solo si el PDF es escaneo o tabla-imagen.

## Quick path (UI)

1. Dataset LedgerLens → PDF parser = **Naive**.
2. Subir los cuatro PDFs de `examples/synthetic/`.
3. Checklist E2E del README.

## Details

| Tema | Decisión |
|------|----------|
| Default | Naive |
| Fallback | DeepDoc (en la imagen) |
| Extra | PaddleOCR (profile `paddleocr`) |
| Dump | `research/extract-ragflow-select-pdf-parser.json` |

## Checklist

- [x] `pdftotext` extrae los hechos (`./scripts/check.sh`)
- [x] README first-run = Naive
- [ ] E2E in-corpus en host ≥16 GB (Rosario / 18.400)
- [ ] Empty response sin evidencia

## Next step

El ingest Naive se verifica en [e2e-16gb.md](e2e-16gb.md), no en esta PC.
