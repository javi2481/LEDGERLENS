# Tasks: Finance P&L neighbor claims

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~700–1100 (evals JSON) |
| 400-line budget risk | High |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| 1 | OpenSpec + lines + signed money + extract claims | `pytest tests/test_extract.py tests/test_finance_lines.py` | pdftotext | `schemas/finance_lines.py`, recipe gold, money.py |
| 2 | Lookup metric + identity_v2 + docs | `pytest tests/test_evals_v2.py tests/test_lookup.py` | `./scripts/check.sh` | lookup, evals/identity_v2.json, README |

## Phase 1: SDD + extract

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 Line catalog + signed_ars + extra claims from page 4
- [x] 1.3 Recipe gold for 1T26/2T26 neighbor rows

## Phase 2: Lookup + evals

- [x] 2.1 Lexical metric routes; no-controlante ≠ neto
- [x] 2.2 identity_v2.json + pytest; v1 green
- [x] 2.3 README + docs/testing.md
