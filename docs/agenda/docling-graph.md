# Overlay de hechos (demo)

En el repo del demo. **No** va en `scripts/up.sh` ni en Compose. **No** re-parsea los PDFs de `demo_4` ni toca MinerU.

Lee un PDF con Docling local, extrae fichas, y `scripts/push_hechos_to_demo4.py` las inyecta como un chunk en `demo_4` para que `chat_demo_4` las use. El parser MinerU de los EEFF no se toca.

## Quick path

1. `pip install docling-graph` (sin extra `vlm`).
2. `python scripts/run_docling_graph_eeff.py` (1T26) o `--preset 2t26`.
3. El runner convierte **solo la página 4, sin OCR** (el EEFF es digital; el OCR default de Graph rompe RapidOCR/torch; las 81 páginas OOM en TableFormer). El oro está en esa página del consolidado.
4. Contrato **direct** (un llamado), markdown, `max_output_tokens=4096` (si no, Graph pide 131072 de salida y se niega a llamar). Overlay: `openai/gpt-oss-120b` (8k TPM). El 8b free es 6k TPM y Graph pide ~7k. El chat sigue en `llama-3.3-70b-versatile`. Override: `GRAPH_GROQ_MODEL`.
5. Para el chat: `python scripts/push_hechos_to_demo4.py` (chunk manual en `demo_4`, prompt de `chat_demo_4`).

## Criterio de merge

1T26 **PASÓ** (rama, no merged): dos nodos distintos, página 4, provenance verbatim:

- consolidado RESULTADO NETO = **21.262.335** (`BYMA|2026-03-31|consolidado|resultado_neto`)
- controlante / atribuible = **21.259.769** (`BYMA|2026-03-31|controlante|resultado_atribuible_controladora`)

Siguiente: EEFF 2T26 **PASÓ** (página 4): consolidado **81.956.525** vs controlante **81.946.993**, período `2026-06-30`. El consolidado 2T26 quedó con provenance `document` (igual `fuente_pagina=4`); el controlante sí es verbatim sobre la tabla.

Graph **no** reemplaza el chat. **No** va en `up.sh`. El README del demo lo lista como overlay, no como parser.

## Config

`backend="llm"`, `inference="remote"` (misma `GROQ_API_KEY` del `.env`, no commitear), `extraction_contract="direct"`, `llm_input_format="markdown"`, `provenance="standard"`. Modelo overlay: `openai/gpt-oss-120b`. Plantilla: `templates.EeffByma`.
