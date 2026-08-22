# presentation-evals Specification

## ADDED Requirements

### Requirement: Dedicated eval file

Cases MUST live in `evals/presentation_v1.json`. Pytest MUST score exact match. identity_v1, identity_v2, and press_v1 MUST stay green.

#### Scenario: Partitions

- GIVEN presentation_v1
- WHEN pytest runs
- THEN 1T26/2T26 EBITDA and LTM cases MUST pass
- AND at least one abstain covers EEFF-metric + presentación
- AND at least one abstain covers P&L + memoria
