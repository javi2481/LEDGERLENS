# Proposal: Finance P&L neighbor claims

> **Change activo (producto).** No inflar [`ledgerlens-idp-kernel`](../ledgerlens-idp-kernel/) ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

The finance plugin only distinguishes net income consolidado vs controlante. Neighboring P&L rows (bruto, operativo, EBT, impuesto, no controlante) are still easy to mix. LedgerLens MUST project those rows as distinct claims from the same page-4 extract, without embeddings.

## Scope

### In Scope

- Line catalog for a closed set: bruto, operativo, antes de impuesto, impuesto a las ganancias, no controlante
- Keep `FinancialStatement` as the net-income gate; do not add six DTO fields
- Parenthetical negatives (`(14.950.948)` → `-14950948`)
- Lexical lookup routes for those metrics; 2T26 first amount column
- `evals/identity_v2.json` + pytest; `identity_v1` stays green
- README + `docs/testing.md` in the same work unit

### Out of Scope

Ingresos/costos/gastos/EPS, SQLite, second domain, capa 3 RAG, MinerU, LLM extract, `app.py` / `ledger_lens/`, Compose, `push_hechos.py`, `hechos_eeff.json`.

## Capabilities

### New Capabilities

- `pnl-extract`: Match closed P&L lines on the selected page; first amount; digits on page.
- `pnl-lookup`: Question → metric + scope + period; “no controlante” is not neto.
- `pnl-evals`: identity_v2 exact-match; v1 regression.

### Modified Capabilities

- `identity-lookup`: metric filter; no-controlante route.

## Approach

Catalog of include/exclude substrings in the finance plugin. Project extra `Claim`s beside the two net-income claims. Gold lives in `recipes/financial_statement.json`.

## Rollback Plan

Revert this change folder plus plugin files (`finance_lines.py`, recipe gold keys, lookup metric, evals v2, tests/docs). Kernel v1 behavior remains.

## Success Criteria

- 1T26 bruto `60144176` ≠ operativo `70223471` ≠ neto `21262335`
- impuesto 1T26 `-14950948`; no controlante `2566` ≠ controlante
- 2T26 first column; identity_v1 still passes; no RAGFlow in tests
