# press-evals Specification

## Purpose

Exact-match evals for press identities. Finance identity_v1/v2 remain the regression suite.

## Requirements

### Requirement: Dedicated eval file

Press cases MUST live in `evals/press_v1.json`, not in `docs/hechos_eeff.json`. Pytest MUST score identity/value/period/page by exact match.

#### Scenario: Partitions

- GIVEN press_v1
- WHEN pytest runs
- THEN date and period identity cases MUST pass
- AND at least one abstain case MUST cover EEFF-metric + comunicado

### Requirement: Finance evals unchanged

identity_v1 and identity_v2 MUST stay green without rewriting their comunicado abstain gold.
