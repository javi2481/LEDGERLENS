# Proposal: Local claim store

> **Change activo (producto).** No inflar [`ledgerlens-idp-kernel`](../ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](../ledgerlens-finance-pnl-claims/), ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

`idp_ask.py` re-runs `pdftotext` on the whole corpus for every question. Lookup MUST read a local claim cache and re-extract only when a PDF changed or the caller forces refresh.

## Scope

### In Scope

- JSON cache under `outputs/` (gitignored); fingerprint PDFs by name + size + mtime
- CLI reads the store; `--refresh` forces extract
- Pytest: cache hit skips extract; identity_v1/v2 still extract in tests
- README + handoff in the same work unit

### Out of Scope

Postgres, SQLite, second domain, capa 3 RAG, MinerU, Compose, `hechos_eeff.json`, `app.py` / `ledger_lens/`

## Capabilities

### New Capabilities

- `claim-store`: Load/save claims; freshness; force refresh.

### Modified Capabilities

None (eval harness keeps calling extract directly).

## Approach

New `schemas/store.py`. Default file `outputs/claims.json`. Evals stay gold-first and ignore the cache.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `schemas/store.py` | New | Cache load/save |
| `scripts/idp_ask.py` | Modified | Read store |
| `tests/test_store.py` | New | Hit / miss / stale / force |
| `README.md`, `docs/` | Modified | Quick path + next slice |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Stale cache after recipe change | Med | `--refresh`; fingerprint only PDFs (docs note: bump via refresh) |
| Corrupt JSON | Low | Treat as miss and rewrite |

## Rollback Plan

Delete this change folder, `schemas/store.py`, `tests/test_store.py`; restore `idp_ask.py` to always extract.

## Success Criteria

- [ ] Second CLI question against unchanged PDFs does not call extract
- [ ] Changed PDF or `--refresh` re-extracts
- [ ] identity_v1 and identity_v2 still pass
- [ ] No RAGFlow / Compose / overlay in this slice
