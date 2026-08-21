# Proposal: Press-release EBITDA LTM margin

> **Shipped.** No inflar. El change activo es [`ledgerlens-rag-pilot`](../ledgerlens-rag-pilot/).

## Intent

The deck already has typed LTM margin (`76` / `75`). The comunicado states the same percentage in prose. Claimprint MUST extract that line as a press claim so identity can cite two documents — without embeddings, without deck P&L, and without fattening `push_claims.py`.

## Scope

### In Scope

- `press_ebitda_margin_ltm` from comunicado page that says `EBITDA (LTM)` / `EBITDA (últimos 12 meses)`
- Gold 1T26 `76`, 2T26 `75`; evals in `press_v1.json`
- Lookup: margen/LTM del comunicado; bare “EBITDA del comunicado” still abstains
- Pytest: press LTM equals presentation LTM for the same period

### Out of Scope

Press P&L table (millones), deck slide-2 P&L, AuC, Voyage/Infinity for identity, UVDoc, Whoosh, inject rewrite

## Capabilities

### New Capabilities

- `press-ltm`: Percentage LTM from press prose; not a money amount.

### Modified Capabilities

- `press-extract`: still date + period on page 1; LTM may be another page.
- `press-lookup`: LTM intent before the generic 1T26 neto default.

## Approach

Same plugin `schemas/press_release.py`. Scan MinerU pages for the LTM regex. Claims keep `scope=comunicado`. Presentation plugin unchanged.

## Rollback Plan

Revert this folder, the new metric/claim/evals/docs. Date/period extract stays.

## Success Criteria

- [ ] Comunicado 1T26 LTM `76` page 2; 2T26 `75`
- [ ] Same values as presentation gold for that period
- [ ] Neto “del comunicado” still abstains
- [ ] `./scripts/check.sh` green without Docker
