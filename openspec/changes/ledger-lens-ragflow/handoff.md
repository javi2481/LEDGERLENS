# Handoff Gentle AI — 2026-08-17

Change activo: `ledger-lens-ragflow`. No archivar. Tasks del change original siguen checked; Graph es **overlay de producto**, no un change SDD nuevo.

## Persistencia

- GitHub `main`: overlay Graph + push a todos los chats.
- Engram `ledgerlens`: session summaries + decisiones (umbral 0.3, no LiteLLM en recaps, Graph fuera de Compose).
- Este archivo: estado para retomar en Linux.

## Demo vigente

Parser MinerU `pipeline`. Embed/rerank Voyage. Motor Infinity. RAGFlow **v0.26.4**. Chat Groq `llama-3.3-70b-versatile` (documentado). Dataset `demo_4`, assistant `chat_demo_4`.

Graph: CLI + plantilla Pydantic; `scripts/push_hechos.py` post-MinerU. Show Quote al EEFF, no a sidecar markdown.

## Siguiente (no es task del change original)

Elegir gancho de integración: catálogo / umbral / página. Ver `docs/agenda/graph-nativo.md` y `docs/handoff-linux.md`.

Verify histórico en Linux 7 GB (`verify-report.md`) **no** es evidencia del demo Windows 32 GB. No re-correrlo como prueba actual.
