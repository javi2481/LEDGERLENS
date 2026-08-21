# MinerU pipeline — parser default (aplicado)

Parser default de LedgerLens para PDFs con tablas y layout (EEFF, filings). Backend **`pipeline`** (CPU). No es hybrid ni VLM.

RAGFlow v0.26.4 es cliente remoto: `MINERU_APISERVER=http://mineru-api:8000` → `POST /file_parse`. `MINERU_BACKEND=pipeline`.

[Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser). [FAQ MinerU](https://ragflow.io/docs/faq#how-to-use-mineru-to-parse-pdf-documents). Dumps: `research/search-mineru-ragflow.json`, `research/search-mineru-hybrid.json`.

## Runbook UI (`demo_4`)

El compose solo deja el API. El parser se snapshottea en cada file al **subir**. Orden fijo:

1. Stack up. Esperar `mineru-api` healthy. Primera vez baja modelos (tarda). Health en el host: `curl http://127.0.0.1:8000/health` y `curl -I http://127.0.0.1:8000/openapi.json`.
2. **Model providers:** con las vars en `.env`, RAGFlow puede auto-provisionar MinerU OCR. Si no aparece, agregalo a mano (FAQ).
3. Crear knowledge base **`demo_4`**. No reusar `demo_3` (files parseados con otro parser).
4. **Configuración primero:**
   - Chunk: **General**
   - PDF parser: **MinerU** (no DeepDOC)
   - Idioma: **Spanish**
   - Knowledge graph y RAPTOR: **Not generated**
   - Chunk tokens: **512**
5. **Después** subir `docs/archivos_muestra/*.pdf`.
6. En **cada** file: clic **General** (columna Parse, no el play) → **Tamaño de la tarea por página = 128**. En v0.26.4 el cliente MinerU manda el PDF entero (`start_page_id=0`). 128 = 1–2 pasadas. Default 12 = muchas pasadas + chunks duplicados.
7. Parse **de a uno**. Log bueno: `[MinerU] invoke api: http://mineru-api:8000/file_parse`. `OCR started` = DeepDoc.
8. Exportar artefactos del kernel: `python scripts/export_mineru.py` (pisa `fixtures/mineru/`). No re-llamar `/file_parse` si el dataset ya está DONE.

Orden de archivos: comunicados → transcripción → presentaciones → EEFF → Memorias.

No hay script de reparse. Un clone de git trae `fixtures/mineru/`; **no** trae volúmenes Docker ni chunks de `demo_4`.

## Details

| Tema | Decisión |
|------|----------|
| Default | MinerU `pipeline` vía sidecar CPU |
| Imagen | `docker/mineru/Dockerfile` (`mineru[pipeline]==3.4.5`). No `mineru:latest` (GPU/vLLM) |
| DNS | `mineru-api:8000` desde `ragflow-cpu`, no `localhost` |
| Hybrid | Fuera. Pide GPU; RAGFlow v0.26.4 no lista `hybrid-engine` |
| Fallback | Naive (texto). DeepDoc (escaneo) |
| Timeout cliente | 1800 s (RAGFlow). Memorias en CPU igual tardan |

## Checklist

- [x] Sidecar en `docker-compose.overlay.yml` (sin profile)
- [x] `MINERU_APISERVER` + `MINERU_BACKEND=pipeline` en `.env.example`
- [x] README first-run = MinerU + `demo_4`
- [x] `mineru-api` healthy
- [x] Parse `demo_4` de a uno (10 PDFs BYMA; comunicados primero; EEFF; Memoria al final)
- [x] Si MinerU cae, ingest falla visible; no inventar texto
