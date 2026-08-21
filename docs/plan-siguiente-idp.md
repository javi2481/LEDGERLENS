# Plan siguiente

**Un solo dominio: finanzas.** Corpus = [`docs/archivos_muestra/`](archivos_muestra/). No se agregan PDFs de otros dominios.

Handoff: [handoff-linux.md](handoff-linux.md). Cierre: [cierre-academico.md](cierre-academico.md). No inflar kernel, P&L, claim-store, press-release, mineru-parse, results-presentation ni el pin RAGFlow.

## Ya cubierto

| Receta | PDFs | Qué extrae |
|--------|------|------------|
| `financial_statement` | EEFF 1T26 / 2T26 | P&L tipado |
| `press_release` | comunicados 1T26 / 2T26 | fecha + período + margen EBITDA LTM |
| `results_presentation` | presentaciones 1T26 / 2T26 | EBITDA + margen LTM |

HITL + dossier HTML + sonda de orientación (skip sin Paddle). Piloto RAG: 20 qrels + 10 chat (skip sin stack). Retrieval: Infinity keyword+vector (docs, no un BM25 propio).

## Cerrado (salvo bugs)

El MVP académico de código está cerrado. Piloto de escritorio **corrido**: métricas en el README (retrieval Recall@5/10 0.25; chat answer 0.6).

| Receta | PDFs | Nota |
|--------|------|------|
| `earnings_transcript` | transcripción 2T26 | **No extract** en este cierre |
| `annual_report` | memorias | **No** extraer P&L |

Change activo: [`ledgerlens-rag-pilot`](../openspec/changes/ledgerlens-rag-pilot/).

## Fuera

Otros dominios, ontología universal, más filas P&L del EEFF, Compose en ~7 GB, branding, vLLM, UVDoc, Whoosh, UI propia, score ML.
