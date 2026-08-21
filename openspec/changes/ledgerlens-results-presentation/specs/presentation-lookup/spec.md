# presentation-lookup Specification

## ADDED Requirements

### Requirement: Presentation intent before narrative

Questions for EBITDA or LTM EBITDA margin of the presentación MUST select `presentacion|presentation_ebitda` or `presentacion|presentation_ebitda_margin_ltm` before the narrative token `presentacion de resultados`.

#### Scenario: 1T26 EBITDA

- GIVEN extracted presentation claims
- WHEN asked for the EBITDA de la presentación 1T26
- THEN the value MUST be `72128`

### Requirement: EEFF-from-presentation and memoria P&L abstain

Presentación + neto/impuesto/bruto/operativo/consolidado MUST abstain. Memoria + resultado/neto MUST still abstain.

#### Scenario: Neto de la presentación

- WHEN asked for resultado neto consolidado de la presentación
- THEN the route MUST be abstain
