# Handoff Gentle AI — 2026-08-17

> **Congelado (pin del demo).** Change `claimprint-ragflow`: no archivar (el pin tiene que seguir en el repo), no inflar. Producto: `openspec/changes/claimprint-idp-kernel/`. Siguiente paso de producto ≠ gancho Graph nativo.
> **Live SoT (2026-08-22+):** chat **Mistral** `mistral-small-latest`, thr **0.2** — ver README / v1.0.1+.

Change original del demo RAGFlow. Tasks del pin siguen checked. Overlay Graph es del **demo**, no del kernel IDP.

## Persistencia

- GitHub `main`: overlay Graph + push a todos los chats.
- Engram `Claimprint`: session summaries + decisiones (umbral **0.2**, no LiteLLM en recaps, Graph fuera de Compose).
- Este archivo: estado para retomar en Linux.

## Demo vigente

Parser MinerU `pipeline`. Embed/rerank Voyage. Motor Infinity. RAGFlow **v0.26.4**. Chat Mistral `mistral-small-latest` (documentado; thr **0.2**). Dataset `demo_4`, assistant `chat_demo_4`.

Graph: CLI + plantilla Pydantic; `scripts/push_hechos.py` post-MinerU. Show Quote al EEFF, no a sidecar markdown.

## Siguiente (no es task de este pin)

Diferidos del demo: `docs/agenda/`. El kernel IDP no se diseña acá.

Verify histórico en Linux 7 GB (`verify-report.md`) **no** es evidencia del demo Windows 32 GB. No re-correrlo como prueba actual.
