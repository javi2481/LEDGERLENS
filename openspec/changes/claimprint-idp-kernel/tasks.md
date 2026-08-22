# Tasks: Claimprint IDP kernel (extract + identity)

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~900–1200 authored (evals JSON + tests) |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | Single PR (`size:exception`; kernel+evals are one contract) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: size-exception
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Kernel + extract + lookup + evals + docs | single (`size:exception`) | `python -m pytest tests/ -q` | `./scripts/check.sh` (pdftotext; no Docker) | `schemas/`, `evals/`, `tests/`, `scripts/idp_ask.py`, `scripts/check.sh`, `pytest.ini`, OpenSpec change, README, `docs/testing.md` |

## Phase 1: OpenSpec + kernel

- [x] 1.1 Write proposal/design/specs/tasks under `openspec/changes/claimprint-idp-kernel/`
- [x] 1.2 Relax `schemas/catalog.py`; add Claim + classify; `needs_graph` delegates
- [x] 1.3 RED: subprocess uses argv list, not shell string from filename

## Phase 2: Extract + lookup

- [x] 2.1 Page select + `pdftotext` fill `FinancialStatement` + reject
- [x] 2.2 Project two claims; lexical lookup; default consolidado
- [x] 2.3 CLI `scripts/idp_ask.py`

## Phase 3: Evals

- [x] 3.1 `evals/identity_v1.json` (~35 KPI + 10 narrative skip)
- [x] 3.2 pytest extract/lookup/evals; `check.sh` runs pytest

## Phase 4: Docs

- [x] 4.1 README rumbo IDP + how to run evals
- [x] 4.2 `docs/testing.md`: capa 2 is the IDP contract
