# Tasks: Results-presentation identity plugin

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350–450 |
| 400-line budget risk | Medium |
| Delivery strategy | single-pr |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| 1 | Plugin + evals | `pytest tests/test_results_presentation.py tests/test_evals_presentation.py` | `./scripts/check.sh` | plugin, recipe, classify, lookup, evals |

## Phase 1: SDD + extract

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 Classify deck; schema + gold; no FinancialStatement from deck/memoria
- [x] 1.3 Corpus dispatch

## Phase 2: Lookup + evals + docs

- [x] 2.1 Presentation intent; abstain traps
- [x] 2.2 `evals/presentation_v1.json` + pytest; v1/v2/press green
- [x] 2.3 README/handoff/check.sh pointers
