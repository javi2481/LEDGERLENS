# identity-lookup Specification

## Purpose

Resolve a Spanish question to typed claims and provenance without embeddings or RAGFlow. Narrative questions are out of this capability (skipped).

## Requirements

### Requirement: Claims from a valid statement

A valid `FinancialStatement` MUST project to two claims with identity keys `ISSUER|YYYY-MM-DD|consolidado|resultado_neto` and `ISSUER|YYYY-MM-DD|controlante|resultado_atribuible_controladora`.

#### Scenario: 1T26 keys

- GIVEN a valid BYMA statement for `2026-03-31`
- WHEN projected
- THEN both identity keys MUST be present and MUST hold distinct amounts

### Requirement: Default consolidado

If the question asks for net income / the period / a quarter and does NOT mention controlante, atribuible, or propietarios, the system MUST select consolidado.

#### Scenario: Trap wording

- GIVEN extracted 1T26 and 2T26 claims
- WHEN asked "¿Cuál es el resultado neto del período?" for 1T26
- THEN the value MUST be `21262335` and MUST NOT be `21259769` or `22362983`

### Requirement: Explicit controlante

Questions that mention controlante, atribuible, or propietarios (and not “no controlante”) MUST select the parent identity.

#### Scenario: 1T26 controlante

- GIVEN extracted claims
- WHEN asked for resultado atribuible a la controlante 1T26
- THEN the value MUST be `21259769`

### Requirement: Period comparison integrity

Comparisons MUST use the same identity scope in every period. Mixing consolidado of one period with controlante of another MUST NOT occur.

#### Scenario: Compare consolidado 1T vs 2T

- GIVEN both filings extracted
- WHEN asked to compare resultado neto consolidado 1T26 vs 2T26
- THEN values MUST be `21262335` and `81956525`

### Requirement: Abstain off-identity

Off-corpus or non-extractable document questions MUST abstain. The system MUST NOT call RAGFlow.

#### Scenario: YPF price

- GIVEN the identity store from sample EEFF only
- WHEN asked for YPF closing price on 3 January
- THEN the result MUST abstain
