# press-extract Specification

## Purpose

Fill two press-release identities from page 1 of a BYMA comunicado. Must not project P&L amounts from that PDF.

## Requirements

### Requirement: Closed field set

The plugin MUST extract `press_as_of_date` and `press_period` only. It MUST NOT extract `resultado_neto`, `impuesto_ganancias`, ingresos, or other P&L lines from the comunicado table.

#### Scenario: 1T26 date and period

- GIVEN `BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf`
- WHEN extracted
- THEN as-of MUST be `2026-05-08`
- AND period MUST be `2026-03-31`
- AND no claim metric MAY be `resultado_neto` or `impuesto_ganancias` from this PDF

### Requirement: 2T26

- GIVEN `BYMA-Comunicado_de_Prensa-2T26.pdf`
- WHEN extracted
- THEN as-of MUST be `2026-08-07`
- AND period MUST be `2026-06-30`

### Requirement: Not a FinancialStatement

A comunicado MUST NOT fill `FinancialStatement`.

#### Scenario: extract_financial_statement

- GIVEN the 1T26 comunicado
- WHEN `extract_financial_statement` runs
- THEN the result MUST be none
