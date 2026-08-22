# pnl-evals Specification

## Purpose

Prove neighbor-row identities independently of RAG. Keep identity_v1 as regression.

## Requirements

### Requirement: v2 gold file

The repo MUST include `evals/identity_v2.json` with identity, neighbor, comparison, and abstention cases. Numeric expectations MUST match `recipes/financial_statement.json`.

#### Scenario: File loadable

- GIVEN the repository root
- WHEN identity_v2 is loaded
- THEN it MUST contain neighbor-row cases and MUST NOT replace identity_v1

### Requirement: v1 still passes

Pytest MUST still score identity_v1. Tests MUST NOT contact RAGFlow.

#### Scenario: check.sh

- GIVEN pdftotext and pytest
- WHEN `./scripts/check.sh` runs
- THEN both v1 and v2 harnesses MUST run
