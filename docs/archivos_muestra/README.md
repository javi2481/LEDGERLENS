# Archivos de muestra (BYMA)

PDFs reales de BYMA para el demo local. Dataset UI: **`demo_4`** (MinerU `pipeline`). Chat: Gemini `gemini-3.1-flash-lite`. Embed: Voyage `voyage-finance-2` (nativo RAGFlow). Rerank: `rerank-2.5-lite`.

Orden: **configurar el dataset** (MinerU, español, KG/RAPTOR off) → **subir** → en cada file **Tamaño de la tarea por página = 128** → **Parse** de a uno. Si subís antes de configurar, cada archivo queda en DeepDOC y hay que borrar y volver a cargar.

No actives Knowledge graph ni RAPTOR: no son parsers y gastan tokens del chat.

Runbook completo: [docs/agenda/mineru-pipeline.md](../agenda/mineru-pipeline.md).

## Orden de parseo

1. Comunicados y transcripción (pocas páginas).
2. Presentaciones.
3. EEFF (tablas; tarda en CPU).
4. Memorias (~190 páginas; al final).

No reusar `demo_3` ni files ya parseados con Docling/DeepDoc/Naive: **dataset nuevo**, subir de nuevo después de poner MinerU en Configuración. Cambiar el dropdown del dataset no reescribe el parser de cada file ni los chunks.

Un clone de GitHub no trae el índice. El parseo previo vive en volúmenes Docker de esta máquina.
