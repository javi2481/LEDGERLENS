# Overlay de hechos (rama `feat/docling-graph-eeff`)

Experimento. **No** está shipped. **No** va en `scripts/up.sh`. **No** toca `demo_4` ni MinerU.

Lee un PDF con Docling local y extrae fichas Pydantic (Groq remoto). El chat `chat_demo_4` se queda.

## Quick path

1. `pip install docling-graph` (sin extra `vlm`).
2. `python scripts/run_docling_graph_eeff.py` — un PDF: `docs/archivos_muestra/BYMA_-_EEFF_31-03-2026_VF.pdf`.
3. El runner convierte **solo la página 4, sin OCR** (el EEFF es digital; el OCR default de Graph rompe RapidOCR/torch; las 81 páginas OOM en TableFormer). El oro está en esa página del consolidado.
4. Contrato **direct** (un llamado), markdown. Dense eran 32 lotes × ~36k tokens: no entra en Groq free (70b = 100k TPD / 12k TPM). El chat `chat_demo_4` sigue en `llama-3.3-70b-versatile`. El overlay usa `llama-3.1-8b-instant` (o `GRAPH_GROQ_MODEL`).
5. Salida en `outputs/graph-1t26/` (gitignored).

## Criterio de merge

Dos nodos distintos, con página:

- consolidado RESULTADO NETO = **21.262.335**
- controlante / atribuible a propietarios = **21.259.769**

Recién ahí el EEFF 2T26. Si el run falla, esta rama queda; `main` sigue siendo el chat.

## Config

`backend="llm"`, `inference="remote"` (misma `GROQ_API_KEY` del `.env`, no commitear), `extraction_contract="direct"`, `llm_input_format="markdown"`, `provenance="standard"`. Modelo overlay: `llama-3.1-8b-instant`. Plantilla: `templates.EeffByma`.
