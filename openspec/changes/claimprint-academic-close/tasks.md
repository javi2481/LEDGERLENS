# Tasks: Academic close

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~450–650 authored |
| 400-line budget risk | Medium |
| Delivery strategy | single-pr |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No if under 400 authored after OpenSpec; split review vs docs if over.

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| A | OpenSpec + pointers | files exist | N/A | change folder |
| B | HITL review | `pytest tests/test_review.py` | N/A | review.py, review_pack |
| C | Dossier | `pytest tests/test_informe.py` | N/A | dossier.py, informe.py |
| D | Preprocess skip | `pytest tests/test_preprocess.py` | desktop optional | preprocess_probe.py |
| E | Docs + check.sh | `./scripts/check.sh` | N/A | docs |

## Phase 1: SDD + HITL

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 `schemas/review.py` + `scripts/review_pack.py` + example JSON + tests

## Phase 2: Dossier + preprocess

- [x] 2.1 `schemas/dossier.py` + `scripts/informe.py` + tests
- [x] 2.2 `scripts/preprocess_probe.py` + skip test

## Phase 3: Docs

- [x] 3.1 README, handoff, testing, plan-siguiente, `docs/cierre-academico.md`, openspec README/config
- [x] 3.2 `scripts/check.sh` contracts; `./scripts/check.sh` green
