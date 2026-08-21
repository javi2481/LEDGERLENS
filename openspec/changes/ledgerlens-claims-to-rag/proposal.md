# Proposal: Inject identity claims into RAGFlow

> **Change activo (producto).** No inflar shipped kernel/P&L/press/mineru-parse, [`ledgerlens-product-shape`](../ledgerlens-product-shape/), ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

Chat overlay gold (`hechos_eeff.json` + Docling Graph) duplicates kernel claims. Claimprint MUST inject those claims into RAGFlow and delete Graph. Identity SoT stays `evals/` + recipes.

## Scope

### In Scope

- `push_claims.py`: claims → EEFF chunk + assistant prompt; strip old Graph markers
- Pytest HTTP mock; no Docker in `check.sh`
- Delete Graph extractor, templates, `hechos_eeff.json`/`.md`, graph agenda
- Generic by scope/metric (presentation claims later need no rewrite)

### Out of Scope

Inflating the RAGFlow pin; Groq eval in CI; presentation plugin; reparse MinerU; custom UI

## Capabilities

### New Capabilities

- `claim-inject`: Kernel claims attached to dedicated EEFF docs; prompt upsert; Show Quote cites the PDF.
- `claim-inject-evals`: Mock `/api/v1`; no chunk on comunicado/memoria/deck.

### Modified Capabilities

None for typed-extract.

## Approach

Pure helpers in `schemas/inject.py`. HTTP in `scripts/push_claims.py`. Source: `load_claims` / `extract_claims_from_dir`. `push_hechos.py` becomes a thin alias.

## Rollback Plan

Revert this folder and restore Graph scripts + `hechos_eeff.json` from git. Kernel extract unchanged.

## Success Criteria

- [ ] Inject builds fichas from claims, not `hechos_eeff.json`
- [ ] Old `Ficha Graph EEFF` chunks are deleted on push
- [ ] `./scripts/check.sh` green; Graph extractor gone
- [ ] README: after merge, run `push_claims.py` on ≥16 GB
