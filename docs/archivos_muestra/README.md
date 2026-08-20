# Archivos de muestra (BYMA)

PDFs reales de BYMA. Los usa **los dos rieles**: el kernel IDP (`pdftotext` / pytest) y el demo RAGFlow (dataset UI **`demo_4`**).

El parseo MinerU de abajo es solo del **demo**. El kernel no necesita Docker.

Orden demo: **configurar el dataset** (MinerU, español, KG/RAPTOR off) → **subir** → en cada file **Tamaño de la tarea por página = 128** → **Parse** de a uno.

No actives Knowledge graph ni RAPTOR: no son parsers y gastan tokens del chat.

Runbook completo: [docs/agenda/mineru-pipeline.md](../agenda/mineru-pipeline.md).

## Orden de parseo

1. Comunicados y transcripción (pocas páginas).
2. Presentaciones.
3. EEFF (tablas; tarda en CPU).
4. Memorias (~190 páginas; al final).

No reusar `demo_3` ni files ya parseados con DeepDoc/Naive: **dataset nuevo**, subir de nuevo después de poner MinerU en Configuración. Cambiar el dropdown del dataset no reescribe el parser de cada file ni los chunks.

Un clone de GitHub no trae el índice. El parseo previo vive en volúmenes Docker de esta máquina.
