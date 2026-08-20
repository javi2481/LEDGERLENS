# pnl-lookup Specification

## Purpose

Route Spanish questions to P&L neighbor metrics without embeddings. Default net-income consolidado MUST stay unchanged when the question does not name another line.

## Requirements

### Requirement: Metric routes

Questions that name resultado bruto, resultado operativo, resultado antes del impuesto, impuesto a las ganancias, or participación no controlante MUST select that metric.

#### Scenario: Gross vs operating

- GIVEN extracted 1T26 claims
- WHEN asked for resultado bruto
- THEN the value MUST be `60144176` and MUST NOT be `70223471` or `21262335`

### Requirement: No controlante is not neto

“No controlante” MUST map to `resultado_no_controlante`, not to consolidado neto and not to controlante.

#### Scenario: 1T26 NCI

- GIVEN extracted claims
- WHEN asked for resultado atribuible a la participación no controlante 1T26
- THEN the value MUST be `2566`

### Requirement: Comparison same metric

Comparisons MUST keep the same metric and scope across periods.

#### Scenario: Gross 1T vs 2T

- GIVEN both filings
- WHEN asked to compare resultado bruto 1T26 vs 2T26
- THEN values MUST be `60144176` and `122610546`
