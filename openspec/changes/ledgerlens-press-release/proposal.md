# Proposal: Press-release identity plugin

> **Change activo (producto).** No inflar [`ledgerlens-idp-kernel`](../ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](../ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](../ledgerlens-claim-store/), ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

The kernel only extracts dedicated EEFF. Comunicados exist in the corpus but classify as `UNKNOWN`. LedgerLens MUST prove a second plugin: typed claims from the press release that are **not** P&L rows.

## Scope

### In Scope

- Classify filenames with `comunicado` as `press_release`
- Extract `press_as_of_date` and `press_period` from page 1 (`pdftotext`)
- Gold 1T26/2T26; ~5–10 evals; identity_v1/v2 still abstain on EEFF metrics “del comunicado”
- Corpus dispatches by recipe; CLI store unchanged

### Out of Scope

P&L figures from the comunicado table, `legal_contract`, SQLite, capa 3 RAG, MinerU, Graph, Compose, `app.py`

## Capabilities

### New Capabilities

- `press-extract`: Page-1 date + reporting period; no net income / tax.
- `press-lookup`: Fecha/período del comunicado; EEFF+comunicado still abstains.
- `press-evals`: exact-match; v1/v2 regression.

### Modified Capabilities

- `typed-extract`: `comunicado` filename is `press_release`, not `UNKNOWN`. Still no `FinancialStatement` from a comunicado.

## Approach

New `schemas/press_release.py`. Receta `extract: true`. Lookup routes for press intent before the generic 1T26 neto default.

## Rollback Plan

Revert this change folder, plugin, recipe gold, classify branch, corpus dispatch, evals, docs. Finance extract stays.

## Success Criteria

- [ ] 1T26 as-of `2026-05-08`; 2T26 as-of `2026-08-07`
- [ ] Period values `2026-03-31` / `2026-06-30`
- [ ] “impuesto del comunicado” and “neto consolidado del comunicado” still abstain
- [ ] identity_v1 and identity_v2 green
