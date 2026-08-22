# identity-evals Specification

## Purpose

Prove extraction and identity independently of RAG. Report metrics by dimension, not a single RAG score.

## Requirements

### Requirement: Structured gold file

The repo MUST include `evals/identity_v1.json` with cases that declare `route`, `question`, and structured expectations (`expected_identity` / `expected_value` / `expected_period` / `expected_source_page` / `expected_abstain` as applicable). Numeric gold MUST match `recipes/financial_statement.json`.

#### Scenario: File exists and is loadable

- GIVEN the repository root
- WHEN the eval file is loaded
- THEN it MUST contain identity, neighbor, comparison, abstention, and narrative-skip cases

### Requirement: Narrative skip

Cases with `route` `narrative` MUST be skipped by the layer-2 harness (capa 3 / RAG).

#### Scenario: Growth question

- GIVEN a narrative case about income growth
- WHEN the identity eval runs
- THEN that case MUST be marked skip and MUST NOT fail identity accuracy

### Requirement: Dimension metrics without RAGFlow

Pytest MUST score Identity, Value, Evidence, Period, Comparison integrity, and Abstention by exact match. Tests MUST NOT contact RAGFlow, Infinity, or Voyage.

#### Scenario: check.sh

- GIVEN `pdftotext` and pytest
- WHEN `./scripts/check.sh` runs
- THEN pytest for this slice MUST run
- AND no RAGFlow HTTP call is required
