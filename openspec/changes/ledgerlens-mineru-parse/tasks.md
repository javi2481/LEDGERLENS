# Tasks: MinerU parse as the only identity path

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~400–700 authored; fixtures generated |
| 400-line budget risk | Medium |
| Delivery strategy | single-pr |
| Chain strategy | none |

### Suggested Work Units

| Unit | Goal | Focused test | Harness | Rollback |
|------|------|--------------|---------|----------|
| 1 | OpenSpec + artifact + classify + extract | `pytest tests/test_extract.py tests/test_classify.py` | fixtures | parse_artifact, classify, extract |
| 2 | Store fingerprint + export script + check.sh + docs | `pytest tests/test_store.py tests/test_evals.py` | `./scripts/check.sh` | store, export, docs |

## Phase 1: SDD + parse + classify

- [x] 1.1 Write proposal/design/specs/tasks
- [x] 1.2 `parse_artifact` + fixtures + export script
- [x] 1.3 Classify cover; extract from artifact; memoria UNKNOWN

## Phase 2: Store + evals + docs

- [x] 2.1 Claim-store fingerprint includes parse hash
- [x] 2.2 Pytest + `check.sh` without identity `pdftotext`
- [x] 2.3 README, handoff, testing, `openspec/config.yaml`
