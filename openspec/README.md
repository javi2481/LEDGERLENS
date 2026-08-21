# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Change **activo (producto):** [`ledgerlens-mineru-parse`](changes/ledgerlens-mineru-parse/).
2. Shipped: [`ledgerlens-idp-kernel`](changes/ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](changes/ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](changes/ledgerlens-claim-store/), [`ledgerlens-press-release`](changes/ledgerlens-press-release/). Pin congelado: [`ledger-lens-ragflow`](changes/ledger-lens-ragflow/).
3. Kernel en cualquier PC: `./scripts/check.sh` (fixtures MinerU). Compose solo en ≥16 GB ([descartado](../docs/agenda/descartado.md) en el Linux de ~7 GB).

## Details

| Tema | Valor |
|------|--------|
| Producto | IDP financiero; corpus = `docs/archivos_muestra/` (BYMA) |
| Demo | Q&A español + citas en RAGFlow; overlay Graph |
| Tests | `./scripts/check.sh` (pytest capa 1–2). E2E RAG no es el DoD |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] README y este archivo nombran el **mismo** change activo (`ledgerlens-mineru-parse`)
- [ ] `ledger-lens-ragflow` sigue marcado congelado
- [ ] `.env` y API keys **no** están en git

## Next step

Handoff: [`docs/handoff-linux.md`](../docs/handoff-linux.md). Dominio = finanzas, corpus = `docs/archivos_muestra/`. Gancho Graph = demo, no producto.
