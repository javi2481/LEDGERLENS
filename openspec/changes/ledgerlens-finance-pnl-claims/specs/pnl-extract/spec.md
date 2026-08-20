# pnl-extract Specification

## Purpose

Fill closed P&L neighbor identities from the same EEFF page used for net income, without growing `FinancialStatement`.

## Requirements

### Requirement: Closed line set

The finance plugin MUST extract `resultado_bruto`, `resultado_operativo`, `resultado_antes_impuesto`, `impuesto_ganancias`, and `resultado_no_controlante` from page text when the net-income gate passes. Ingresos, costos, gastos, and EPS MUST NOT be extracted in this slice.

#### Scenario: 1T26 neighbors

- GIVEN page 4 of `BYMA_-_EEFF_31-03-2026_VF.pdf`
- WHEN lines are extracted
- THEN bruto MUST be `60144176`
- AND operativo MUST be `70223471`
- AND antes de impuesto MUST be `36213283`
- AND impuesto MUST be `-14950948`
- AND no controlante MUST be `2566`
- AND those values MUST be distinct from neto `21262335`

### Requirement: First amount column

The period amount MUST be the first parsed amount on the matched line. Later columns (prior year, 2T26 three-month) MUST NOT be selected as the period figure.

#### Scenario: 2T26 YTD

- GIVEN page 4 of `BYMA - EEFF 30-06-2026.pdf`
- WHEN bruto is extracted
- THEN the value MUST be `122610546` (first column)
- AND MUST NOT be `58533038` (three-month column)

### Requirement: Parenthetical negatives

An amount printed in parentheses MUST be stored with a leading minus. Digits without the sign MUST appear on the page.

#### Scenario: Tax line

- GIVEN `Impuesto a las ganancias` printed as `(14.950.948)`
- WHEN parsed
- THEN the claim value MUST be `-14950948`
