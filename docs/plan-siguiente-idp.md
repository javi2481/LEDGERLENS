# Plan siguiente

**Un solo dominio: finanzas.** Corpus = [`docs/archivos_muestra/`](archivos_muestra/). No se agregan PDFs de otros dominios.

Handoff: [handoff-linux.md](handoff-linux.md). No inflar kernel, P&L, claim-store, press-release, mineru-parse ni el pin RAGFlow.

## Ya cubierto

| Receta | PDFs | Qué extrae |
|--------|------|------------|
| `financial_statement` | EEFF 1T26 / 2T26 | P&L tipado |
| `press_release` | comunicados 1T26 / 2T26 | fecha + período |
| `results_presentation` | presentaciones 1T26 / 2T26 | EBITDA + margen LTM |

## Qué sigue (mismo dominio)

| Receta | PDFs | Nota |
|--------|------|------|
| `earnings_transcript` | transcripción 2T26 | Un solo PDF; después |
| `annual_report` | memorias | **No** extraer P&L |

Change activo: [`ledgerlens-results-presentation`](../openspec/changes/ledgerlens-results-presentation/).

## Fuera

Otros dominios, ontología universal, más filas P&L del EEFF, Compose en ~7 GB, branding, vLLM.
