# OpenSpec / Gentle AI (hybrid)

Claimprint usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

El nombre de producto es **Claimprint** (antes LedgerLens). Los IDs de change (`ledgerlens-*`, `ledger-lens-ragflow`) y el proyecto Engram no se renombran: son rutas.

## Quick path

1. Change **activo:** [`ledgerlens-rag-pilot`](changes/ledgerlens-rag-pilot/).
2. Shipped: [`ledgerlens-idp-kernel`](changes/ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](changes/ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](changes/ledgerlens-claim-store/), [`ledgerlens-press-release`](changes/ledgerlens-press-release/), [`ledgerlens-mineru-parse`](changes/ledgerlens-mineru-parse/), [`ledgerlens-product-shape`](changes/ledgerlens-product-shape/), [`ledgerlens-claims-to-rag`](changes/ledgerlens-claims-to-rag/), [`ledgerlens-results-presentation`](changes/ledgerlens-results-presentation/), [`ledgerlens-academic-close`](changes/ledgerlens-academic-close/), [`ledgerlens-press-ltm`](changes/ledgerlens-press-ltm/). Pin UI/stack: [`ledger-lens-ragflow`](changes/ledger-lens-ragflow/) — no inflar.
3. IDP en cualquier PC: `./scripts/check.sh`. Compose en ≥16 GB. Tras merge en la UI: `python scripts/push_claims.py` y chat nuevo.

## Details

| Tema | Valor |
|------|--------|
| Producto | Claimprint — claims intelligence; instancia BYMA (`docs/archivos_muestra/`) |
| UI | RAGFlow v0.26.4 + Infinity + MinerU + Voyage + Groq |
| Tests | `./scripts/check.sh` (pytest identidad). Chat live no es el DoD del IDP |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] Este archivo nombra el change activo (`ledgerlens-rag-pilot`). El README de producto no apunta a IDs `ledgerlens-*` (solo nota de IDs internos).
- [ ] `ledger-lens-ragflow` sigue siendo el pin de UI/stack (sin trabajo IDP adentro)
- [ ] `.env` y API keys **no** están en git

## Next step

Handoff: [`docs/handoff-linux.md`](../docs/handoff-linux.md).
