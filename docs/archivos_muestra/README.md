# Archivos de muestra (BYMA)

PDFs reales de BYMA para el demo local. Dataset UI: `demo_2` (limpio, Docling Serve). Chat: OpenRouter Nano. Embed: Voyage `voyage-finance-2`. Rerank: `rerank-2.5-lite`.

Orden: **configurar el dataset** (Docling, KG/RAPTOR off) → **subir** → **Parse** de a uno. Si subís antes de configurar, cada archivo queda en DeepDOC y hay que borrar y volver a cargar.

No actives Knowledge graph ni RAPTOR: no son parsers y gastan tokens del chat.

## Orden de parseo

1. Comunicados y transcripción (pocas páginas).
2. Presentaciones.
3. EEFF (tablas; tarda en CPU).
4. Memoria 2025 (190 páginas; al final).

Los archivos ya parseados con Naive o DeepDoc hay que **borrar y volver a subir** después de poner Docling en Configuración. Cambiar el dropdown del dataset no reescribe el parser de cada file ni los chunks.

Un clone de GitHub no trae el índice. El parseo previo vive en volúmenes Docker de esta máquina.
