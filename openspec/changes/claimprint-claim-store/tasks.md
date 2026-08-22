# Tasks: Local claim store

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~250–400 |
| 400-line budget risk | Low |
| Delivery strategy | single-pr |
| Chain strategy | none |

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| 1 | OpenSpec + store + CLI + tests + docs | `pytest tests/test_store.py` | `./scripts/check.sh` | `schemas/store.py`, `idp_ask.py`, tests, this change |

## Phase 1: SDD + store

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 `schemas/store.py`: fingerprint, load/save, corrupt → miss
- [x] 1.3 `idp_ask.py` reads store; `--refresh`

## Phase 2: Tests + docs

- [x] 2.1 `tests/test_store.py` hit / miss / stale / force
- [x] 2.2 identity_v1 and identity_v2 still green
- [x] 2.3 README, handoff, plan-siguiente-idp, OpenSpec README
