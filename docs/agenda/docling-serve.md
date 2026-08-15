# Docling Serve — parser clásico (aplicado)

Parser default de LedgerLens para PDFs con tablas y layout (EEFF, filings). **No** es el pipeline VLM (Granite-Docling). Es layout Heron + TableFormer en CPU.

RAGFlow es cliente remoto: `DOCLING_SERVER_URL=http://docling-serve:5001` → Docling Serve `/v1/convert/source`. `USE_DOCLING=false` (no in-process en `ragflow-cpu`). MinerU y OpenDataLoader están [descartados](descartado.md). Naive queda como fallback.

[Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser). [FAQ Docling Serve](https://ragflow.io/docs/faq). Dumps: `research/extract-ragflow-select-pdf-parser.json`, `research/extract-docling-classic-vlm.json`, `research/search-docling-classic-parser.json`.

## Quick path

1. Sidecar Compose: `quay.io/docling-project/docling-serve-cpu:v1.30.0`, puerto **5001**. DNS interno `docling-serve`, no `localhost` desde `ragflow-cpu`.
2. `.env`: `DOCLING_SERVER_URL=http://docling-serve:5001`, `USE_DOCLING=false`.
3. Dataset → Configuración **primero**: Reconocimiento de disposición = **Docling**. Knowledge graph y RAPTOR apagados (Not generated).
4. **Después** subir los PDFs. En cada file, clic en **General** (columna Parse) → **Tamaño de la tarea por página** = **128** (máximo de la UI; default 12). Con Docling Serve cada slice convierte el PDF entero.
5. **Por último** Parse, de a uno. En el log: `[Docling] Requesting external server`. `OCR started` = DeepDoc. Un clone de git no trae chunks.

## Details

| Tema | Decisión |
|------|----------|
| Default | Docling clásico vía sidecar |
| Esta PC | CPU. Imagen `docling-serve-cpu` ~4,4 GB. No GPU. |
| In-process | Evitar (`USE_DOCLING=true`): carga modelos en `ragflow-cpu` |
| VLM | Fuera. Granite-Docling = [vllm.md](vllm.md) cuando haya NVIDIA |
| Graph | Overlay aparte: [docling-graph.md](docling-graph.md). Serve solo convierte |
| watsonx managed | IBM ~US$4 / 1.000 páginas. No es el demo self-host |
| Fallback | Naive. DeepDoc si el PDF es escaneo y Docling no está |
| v0.26.4 remoto | Si Serve ignora `do_chunking`, RAGFlow cae a `md_content` (no 0 chunks silenciosos del bug v0.25.x) |

## Checklist

- [x] Sidecar en `docker-compose.overlay.yml` (sin profile)
- [x] `DOCLING_SERVER_URL` en `.env.example`; `USE_DOCLING=false`
- [x] README first-run = Docling
- [ ] `docling-serve` healthy (`curl http://127.0.0.1:5001/health` en el host)
- [ ] Re-parse `demo_1` con Docling (comunicados primero; EEFF; Memoria al final)
- [ ] Si Serve cae, ingest falla visible; no inventar texto

## Next step

Parsear el corpus de `docs/archivos_muestra/` en esta instancia. No encender Knowledge graph ni RAPTOR. Graph de hechos: [docling-graph.md](docling-graph.md).
