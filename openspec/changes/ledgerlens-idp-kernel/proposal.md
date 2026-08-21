# Proposal: Claimprint IDP kernel (extract + identity)

> **Shipped.** El change activo de producto es [`ledgerlens-finance-pnl-claims`](../ledgerlens-finance-pnl-claims/). El pin del demo RAGFlow está congelado en [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

RAG over chunks picks the wrong neighboring P&L row (consolidado vs controlante) even when MinerU extracted both figures. Claimprint MUST resolve identity from typed claims, not embedding similarity. Finance is the first domain plugin; the kernel MUST stay domain-agnostic.

## Scope

### In Scope

- Generic recipe catalog, Claim, routes `identity` / `abstain` (narrative skipped)
- Deterministic EEFF extract via `pdftotext` + `FinancialStatement` + `reject_financial_statement`
- Lexical question → identity lookup without RAGFlow / Voyage
- Eval set (~35 KPI cases + 10 narrative skip) and pytest; `check.sh` runs pytest
- README + `docs/testing.md` in the same work unit

### Out of Scope

RAGFlow router, Graph overlay as source of truth, Postgres/Neo4j, LLM-as-judge, online evals, extra domain schemas (legal/health), `app.py` / `ledger_lens/`, Gradio, HF Space.

## Capabilities

> sdd-spec contract. `openspec/specs/` empty aside from `.gitkeep`.

### New Capabilities

- `typed-extract`: Classify recipe, select page, fill domain schema, abstain on validation failure.
- `identity-lookup`: Question → identity key → claim + provenance; default consolidado when unspecified.
- `identity-evals`: Layer-1/2 exact-match evals; no RAGFlow; metrics by dimension.

### Modified Capabilities

None

## Approach

Keep RAGFlow demo untouched. Add `schemas/` kernel + `evals/identity_v1.json` + pytest. Project `FinancialStatement` to two claims using `EMISOR|period|scope|metric`. `pdftotext -layout` is the CI parser (no Docker).

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `schemas/` | Modified/New | Catalog relax; Claim; extract; lookup |
| `evals/` | New | Structured gold questions |
| `tests/` | New | Layer 1–2 pytest |
| `scripts/check.sh` | Modified | Run pytest |
| `scripts/graph_hechos.py` | Modified | Reuse classify helper |
| `README.md`, `docs/testing.md` | Modified | IDP kernel + eval contract |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| `pdftotext` misses table cells | Med | Fail if gold digits absent from page text |
| Catalog still finance-locked | Low | Require ≥1 recipe, not `financial_statement` |
| Overlay/demo drift | Low | Do not edit Compose, vendor, `push_hechos.py` |

## Rollback Plan

Revert the change folder and `schemas/` / `evals/` / `tests/` / docs / `check.sh`. Demo RAGFlow unchanged.

## Dependencies

`pdftotext` (poppler), `pytest`, `pydantic`. No RAGFlow runtime.

## Success Criteria

- [ ] Dedicated EEFF 1T26/2T26 extract both net-income identities; non-EEFF recipes do not extract
- [ ] Trap “resultado neto” (no controlante) → consolidado `21262335` / `81956525`
- [ ] Controlante questions → the other row; YPF / comunicado / memoria → abstain
- [ ] Pytest does not call RAGFlow; `./scripts/check.sh` runs it
