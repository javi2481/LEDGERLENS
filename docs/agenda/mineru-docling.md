# MinerU / Docling / OpenDataLoader (agenda)

Parsers experimentales de RAGFlow. Mejoran tablas complejas. RAGFlow es cliente remoto (otro servidor). [Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser).

No son más eficientes. PaddleOCR opcional ya cubre un parser visual extra.

## Quick path

1. Decidir un solo parser extra (no los tres).
2. Levantar su API (MinerU FastAPI, Docling Serve, etc.).
3. Configurar URL en Model providers / `.env`. Dataset parser = ese motor.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | DeepDoc pierde tablas o layout de filings (sintéticos o reales) |
| Costo | Otro contenedor + RAM/GPU |
| Dump | `research/extract-ragflow-select-pdf-parser.json` |
| PaddleOCR | Ya está como profile; probarlo antes que MinerU |

## Checklist

- [ ] DeepDoc E2E falló en tablas, no solo “queremos más parsers”
- [ ] Un servidor reachable desde `ragflow-cpu` (DNS Compose, no `localhost`)
- [ ] Ingest fail visible si el parser cae; no inventar texto

## Next step

Si DeepDoc alcanza el demo sintético, no implementar.
