# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Change **activo (producto):** [`changes/ledgerlens-idp-kernel/`](changes/ledgerlens-idp-kernel/).
2. Change **congelado (pin del demo):** [`changes/ledger-lens-ragflow/`](changes/ledger-lens-ragflow/). No inflarlo. No es el SDD del kernel.
3. Kernel en cualquier PC: `./scripts/check.sh`. Compose solo en ≥16 GB ([descartado](../docs/agenda/descartado.md) en el Linux de ~7 GB).

## Details

| Tema | Valor |
|------|--------|
| Producto | IDP multi-dominio; finanzas es el primer plugin |
| Demo | Q&A español + citas en RAGFlow; overlay Graph |
| Tests | `./scripts/check.sh` (pytest capa 1–2). E2E RAG no es el DoD |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] README y este archivo nombran el **mismo** change activo (`ledgerlens-idp-kernel`)
- [ ] `ledger-lens-ragflow` sigue marcado congelado
- [ ] `.env` y API keys **no** están en git

## Next step

Handoff: [`docs/handoff-linux.md`](../docs/handoff-linux.md). El gancho Graph nativo es diferido del **demo**, no el siguiente paso de producto ([agenda](../docs/agenda/README.md)).
