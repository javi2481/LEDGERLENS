# press-lookup Specification

## Purpose

Resolve questions about the comunicado as a comunicado. EEFF metrics attributed to the press release MUST still abstain.

## Requirements

### Requirement: Date and period intent

Questions that ask for the fecha or período of the comunicado MUST select `comunicado|press_as_of_date` or `comunicado|press_period` for the named quarter.

#### Scenario: 1T26 date

- GIVEN extracted press claims
- WHEN asked for the fecha del comunicado 1T26
- THEN the value MUST be `2026-05-08`

### Requirement: EEFF-from-comunicado abstain

Questions that name comunicado together with resultado neto, consolidado, controlante, resultado bruto, or impuesto MUST abstain. The system MUST NOT answer with press or EEFF amounts.

#### Scenario: Regression

- GIVEN mixed finance + press claims
- WHEN asked for resultado neto consolidado del comunicado or impuesto del comunicado
- THEN the route MUST be abstain
