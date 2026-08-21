# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Change **activo:** [`ledgerlens-academic-close`](changes/ledgerlens-academic-close/).
2. Shipped: [`ledgerlens-idp-kernel`](changes/ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](changes/ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](changes/ledgerlens-claim-store/), [`ledgerlens-press-release`](changes/ledgerlens-press-release/), [`ledgerlens-mineru-parse`](changes/ledgerlens-mineru-parse/), [`ledgerlens-product-shape`](changes/ledgerlens-product-shape/), [`ledgerlens-claims-to-rag`](changes/ledgerlens-claims-to-rag/), [`ledgerlens-results-presentation`](changes/ledgerlens-results-presentation/). Pin UI/stack: [`ledger-lens-ragflow`](changes/ledger-lens-ragflow/) — no inflar.
3. IDP en cualquier PC: `./scripts/check.sh`. Compose en ≥16 GB. Tras merge en la UI: `python scripts/push_claims.py` y chat nuevo.

## Details

| Tema | Valor |
|------|--------|
| Producto | IDP financiero de punta a punta; corpus = `docs/archivos_muestra/` (BYMA) |
| UI | RAGFlow v0.26.4 + Infinity + MinerU + Voyage + Groq |
| Tests | `./scripts/check.sh` (pytest identidad). Chat live no es el DoD del IDP |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] README y este archivo nombran el **mismo** change activo (`ledgerlens-academic-close`)
- [ ] `ledger-lens-ragflow` sigue siendo el pin de UI/stack (sin trabajo IDP adentro)
- [ ] `.env` y API keys **no** están en git

## Next step

Handoff: [`docs/handoff-linux.md`](../docs/handoff-linux.md).
