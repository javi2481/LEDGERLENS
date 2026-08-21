# Tasks: Product shape — one finance IDP

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~200 authored; `research/` delete is generated dumps |
| 400-line budget risk | High (dumps) |
| Delivery strategy | stacked-to-main |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test | Runtime harness | Rollback |
|------|------|-----------|--------------|-----------------|----------|
| 1 | SDD + docs + legal + page_text | PR 1 | `./scripts/check.sh` | N/A docs/catalog | this change folder, recipes, page_text, docs |
| 2 | Delete `research/` + pivot agenda | PR 2 size:exception | `./scripts/check.sh` | N/A | git restore research/ agenda |

## Phase 1: SDD + living docs + catalog

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 Rewrite README, OpenSpec README, config context, handoff, plan-siguiente, testing (one product; Graph still documented as temporary inject)
- [x] 1.3 Remove `legal_contract`; drop asserts; delete `schemas/page_text.py` + test
- [x] 1.4 Point `check.sh` skip text away from deleted `descartado.md`

## Phase 2: Pivot debris

- [x] 2.1 Delete `research/`
- [x] 2.2 Delete pivot agenda files; keep `mineru-pipeline.md`; recut agenda README
- [x] 2.3 `./scripts/check.sh`
