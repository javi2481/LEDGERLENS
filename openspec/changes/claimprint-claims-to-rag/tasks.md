# Tasks: Inject identity claims into RAGFlow

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350–500 authored |
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
| 1 | inject helpers + mock push + delete Graph | `pytest tests/test_inject.py tests/test_push_claims.py` | N/A CI; live ≥16 GB | inject, push_claims, Graph files |

## Phase 1: SDD + helpers

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 `schemas/inject.py` + unit tests
- [x] 1.3 `push_claims.py` + HTTP mock; alias `push_hechos.py`

## Phase 2: Delete Graph + docs

- [x] 2.1 Delete Graph extractor, templates, hechos_eeff, graph agenda
- [x] 2.2 README/testing/handoff: claims inject; mandatory live push
- [x] 2.3 `./scripts/check.sh`
