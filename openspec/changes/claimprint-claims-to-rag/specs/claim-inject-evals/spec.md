# claim-inject-evals Specification

## Purpose

Prove inject wiring without Docker or chat LLM.

## ADDED Requirements

### Requirement: HTTP mock in pytest

Pytest MUST mock RAGFlow `/api/v1` and MUST NOT start Compose. `check.sh` MUST remain green on hosts without Docker.

#### Scenario: Mock attach

- GIVEN mocked datasets with one EEFF name and one comunicado name
- WHEN `push_claims` runs against the mock
- THEN POST chunk MUST target only the EEFF document id
