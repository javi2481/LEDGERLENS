# Proposal: Product shape — one finance IDP

> **Change activo (producto).** No inflar [`ledgerlens-idp-kernel`](../ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](../ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](../ledgerlens-claim-store/), [`ledgerlens-press-release`](../ledgerlens-press-release/), [`ledgerlens-mineru-parse`](../ledgerlens-mineru-parse/), ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

Docs still narrate two products (kernel vs frozen demo) and keep pivot debris (`research/`, legal stub, `pdftotext` identity helper). Claimprint MUST read as one end-to-end finance IDP: RAGFlow UI, MinerU parse, Infinity/Voyage/Groq, typed claims. Graph overlay stays until a later inject change.

## Scope

### In Scope

- Rewrite README, handoff, testing, OpenSpec pointers: one product, two contracts (evals vs chat)
- Delete `research/`, pivot agenda files; keep MinerU pipeline runbook
- Remove `legal_contract` recipe; keep `annual_report` / `earnings_transcript` stubs
- Remove identity `schemas/page_text.py` (`pdftotext`); export bootstrap may still call poppler

### Out of Scope

Graph scripts, `hechos_eeff.json`, `push_hechos.py`, presentation extract, vendor pin, Compose, fixtures, archiving shipped OpenSpec into `openspec/specs/`

## Capabilities

### New Capabilities

- `product-narrative`: Living docs describe one product (RAG UI + typed IDP) over MinerU. RAGFlow pin is the UI/stack pin, not a disposable demo rail.

### Modified Capabilities

None (no extract/lookup requirement change).

## Approach

Docs + catalog cleanup only. `check.sh` skip text must not point at deleted agenda files. Graph docs remain until claims-to-rag.

## Rollback Plan

Revert this folder and the doc/catalog/page_text deletes. Restore `research/` from git. Extract/press/MinerU fixtures unchanged.

## Success Criteria

- [ ] README and `openspec/README.md` name this change as activo
- [ ] No `legal_contract` recipe; `schemas/page_text.py` gone
- [ ] `research/` gone; MinerU pipeline runbook remains
- [ ] `./scripts/check.sh` green
