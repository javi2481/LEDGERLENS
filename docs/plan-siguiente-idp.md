# Plan siguiente (producto IDP)

**Un solo dominio: finanzas.** El corpus es [`docs/archivos_muestra/`](archivos_muestra/) (EEFF, comunicados, presentaciones, transcripción, memorias). No se agregan PDFs de otros dominios. `legal_contract` es stub de clasificador (`extract: false`), no una slice.

Handoff: [handoff-linux.md](handoff-linux.md). No inflar kernel, P&L, claim-store, press-release, mineru-parse ni el pin RAGFlow.

## Ya cubierto

| Receta | PDFs | Qué extrae |
|--------|------|------------|
| `financial_statement` | EEFF 1T26 / 2T26 | P&L tipado |
| `press_release` | comunicados 1T26 / 2T26 | fecha + período (sigue siendo finanzas, no otro dominio) |

## Qué queda en el mismo dominio

| Receta | PDFs | Nota |
|--------|------|------|
| `results_presentation` | presentaciones 1T26 / 2T26 | Siguiente slice natural |
| `earnings_transcript` | transcripción 2T26 | Un solo PDF |
| `annual_report` | memorias | **No** extraer P&L (trampa de evals) |

Siguiente change OpenSpec **nuevo**, si se continúa: presentación de resultados, campos que no copien el EEFF.

## Fuera

Otros dominios (legal, salud, industria), ontología universal, más filas P&L del EEFF, RAG, Graph, Compose en ~7 GB.
