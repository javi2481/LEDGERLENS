# Overlay de hechos (demo)

En el riel **demo**. **No** es el contrato IDP (`evals/identity_v1.json`). **No** va en `scripts/up.sh` ni Compose. **No** re-parsea MinerU.

Lee un EEFF con Docling local, extrae fichas, y `scripts/push_hechos.py` las pega como chunk manual **en cada PDF que las necesite** (Show Quote cita el estado, no un `.md`) y las deja en el prompt de **todos** los chats. Gold de este riel: `docs/hechos_eeff.json`.

## Qué archivos

Graph desambigua **consolidado vs controlante** en un EEFF. Entra solo en filings dedicados (nombre con `EEFF`, sin Memoria/comunicado/presentación/transcripción). Memorias anuales son demasiado grandes (OOM) y la página 4 no es el P&L: pasá `--pdf` y `--pages` a mano.

## Quick path

1. `pip install docling-graph` (sin extra `vlm`).
2. Un filing: `python scripts/run_docling_graph_eeff.py --pdf "docs/archivos_muestra/BYMA - EEFF 30-06-2026.pdf"`. Presets: `--preset 1t26` / `--preset 2t26`. Todos los EEFF de muestra: `--all`.
3. El runner convierte **solo la página 4, sin OCR** (el EEFF es digital; el OCR default de Graph rompe RapidOCR/torch; las 81 páginas OOM en TableFormer). El oro del consolidado está en esa página. Otro emisor: `--pages` si el P&L no es la 4.
4. Contrato **direct** (un llamado), markdown, `max_output_tokens=4096` (si no, Graph pide 131072 de salida y se niega a llamar). Overlay: `openai/gpt-oss-120b` (8k TPM). El 8b free es 6k TPM y Graph pide ~7k. El chat sigue en `llama-3.3-70b-versatile`. Override: `GRAPH_GROQ_MODEL`.
5. Para los chats: `python scripts/push_hechos.py` (recorre **todos** los datasets y **todos** los asistentes). Un chat ya abierto no toma el prompt nuevo: abrí otro. Si creás un asistente nuevo, volvé a correr el push.

## Criterio de merge

1T26 **PASÓ**: dos nodos distintos, página 4, provenance verbatim:

- consolidado RESULTADO NETO = **21.262.335** (`BYMA|2026-03-31|consolidado|resultado_neto`)
- controlante / atribuible = **21.259.769** (`BYMA|2026-03-31|controlante|resultado_atribuible_controladora`)

EEFF 2T26 **PASÓ** (página 4): consolidado **81.956.525** vs controlante **81.946.993**, período `2026-06-30`. El consolidado 2T26 quedó con provenance `document` (igual `fuente_pagina=4`); el controlante sí es verbatim sobre la tabla.

Graph **no** reemplaza el chat. **No** va en `up.sh`. El README del demo lo lista como overlay, no como parser.

## Config

`backend="llm"`, `inference="remote"` (misma `GROQ_API_KEY` del `.env`, no commitear), `extraction_contract="direct"`, `llm_input_format="markdown"`, `provenance="standard"`. Modelo overlay: `openai/gpt-oss-120b`. Plantilla: `templates.EeffByma`.
