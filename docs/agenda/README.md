# Agenda (retomar luego)

Ítems del **riel demo** (RAGFlow / UI / GPU). El producto IDP no vive acá: [handoff](../handoff-linux.md) y [plan siguiente](../plan-siguiente-idp.md).

Consultá un archivo, no todos. Cerrados: [descartado.md](descartado.md).

## Quick path

1. Confirmá que el ítem es del demo, no del kernel.
2. Confirmá el disparador (GPU, chrome UI, LinkedIn).
3. Seguí el checklist. No implementar sin disparador.

## Activo (demo)

| Ítem | Cuándo retomarlo |
|------|------------------|
| [vLLM](vllm.md) | GPU NVIDIA: chat local o MinerU hybrid. |
| [Posicionamiento LinkedIn](posicionamiento-linkedin.md) | Publicar tesis IDP 2026 sin vender hybrid/KG no shipped. |
| [Branding cosmético UI](branding-cosmetic.md) | Chrome LedgerLens sin fork. |
| [Gancho nativo Graph](graph-nativo.md) | Solo el overlay del chat. No es el siguiente paso de producto. |

## Ya hecho (no es agenda)

| Tema | Riel | Estado |
|------|------|--------|
| Kernel IDP capa 1–2 + P&L vecino | producto | `evals/identity_v1.json` + `v2`; ver [handoff](../handoff-linux.md) |
| Overlay **Docling Graph** | demo | no en `up.sh` ([nota](docling-graph.md)) |
| Parser **MinerU** `pipeline` | demo | sidecar `mineru-api:8000` |
| Chat **Groq** / Voyage / Infinity | demo | pin v0.26.4 |
| Tests kernel | producto | `./scripts/check.sh` |

## Next step

Handoff: [handoff-linux.md](../handoff-linux.md). Producto activo: [press-release](../../openspec/changes/ledgerlens-press-release/). Demo diferido = branding o LinkedIn. Gancho Graph **no** es el rumbo. No Compose en Linux ~7 GB.
