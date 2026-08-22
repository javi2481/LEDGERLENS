# Tasks: Press-release identity plugin

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350–500 |
| 400-line budget risk | Medium |
| Delivery strategy | single-pr |
| Chain strategy | none |

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| 1 | OpenSpec + classify + extract + corpus | `pytest tests/test_extract.py tests/test_press_release.py` | pdftotext | plugin, recipe, classify, corpus |
| 2 | Lookup + press_v1 + docs | `pytest tests/test_evals_press.py tests/test_evals.py` | `./scripts/check.sh` | lookup, evals, README |

## Phase 1: SDD + extract

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 Classify `comunicado` → `press_release`
- [x] 1.3 Schema + gold + corpus dispatch; no FinancialStatement from PR

## Phase 2: Lookup + evals + docs

- [x] 2.1 Press intent; EEFF+comunicado abstain stays
- [x] 2.2 `evals/press_v1.json` + pytest; v1/v2 green
- [x] 2.3 README, handoff, plan-siguiente-idp, OpenSpec README
