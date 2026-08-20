# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Changes **shipped (producto):** [`ledgerlens-idp-kernel`](changes/ledgerlens-idp-kernel/) y [`ledgerlens-finance-pnl-claims`](changes/ledgerlens-finance-pnl-claims/).
2. Pin congelado: [`ledger-lens-ragflow`](changes/ledger-lens-ragflow/). Siguiente slice: [`docs/plan-siguiente-idp.md`](../docs/plan-siguiente-idp.md) (aún sin change abierto).
3. Kernel en cualquier PC: `./scripts/check.sh`. Compose solo en ≥16 GB ([descartado](../docs/agenda/descartado.md) en el Linux de ~7 GB).

## Details

| Tema | Valor |
|------|--------|
| Producto | IDP multi-dominio; finanzas es el primer plugin |
| Demo | Q&A español + citas en RAGFlow; overlay Graph |
| Tests | `./scripts/check.sh` (pytest capa 1–2). E2E RAG no es el DoD |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] README y este archivo nombran kernel + P&L como **shipped**, no como work activo
- [ ] `ledger-lens-ragflow` sigue marcado congelado
- [ ] `.env` y API keys **no** están en git

## Next step

Handoff: [`docs/handoff-linux.md`](../docs/handoff-linux.md). Siguiente slice: [`docs/plan-siguiente-idp.md`](../docs/plan-siguiente-idp.md) (persistir claims). Gancho Graph = demo, no producto.
