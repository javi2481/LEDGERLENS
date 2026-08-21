# presentation-extract Specification

## Purpose

Fill two management identities from BYMA results-presentation highlights. Must not project P&L from the deck.

## ADDED Requirements

### Requirement: Closed field set

The plugin MUST extract `presentation_ebitda` and `presentation_ebitda_margin_ltm` only, plus `period`. EBITDA MUST be millions of ARS as digits. Margin MUST be integer percent points without `%`. MUST NOT extract `resultado_neto`, `impuesto_ganancias`, bruto, operativo, ingresos, or AUC.

#### Scenario: 1T26

- GIVEN `Presentación_de_resultados_BYMA-1T26.pdf`
- WHEN extracted
- THEN EBITDA MUST be `72128`
- AND LTM margin MUST be `76`
- AND period MUST be `2026-03-31`

#### Scenario: 2T26

- GIVEN `Presentacion_de_resultados_BYMA-2T26.pdf`
- WHEN extracted
- THEN EBITDA MUST be `71697`
- AND LTM margin MUST be `75`
- AND period MUST be `2026-06-30`

### Requirement: Highlights not slide-2 P&L

Keywords MUST select the block containing `Alcanzamos un EBITDA`. MUST NOT fill from `RESULTADO TRIMESTRAL`.

#### Scenario: Source page

- GIVEN either deck artifact
- WHEN extracted
- THEN `source_page` MUST be the highlights page (page 12 in current fixtures)

### Requirement: Not FinancialStatement; memoria dark

A deck MUST NOT fill `FinancialStatement`. A memoria MUST NOT yield presentation or P&L claims.

#### Scenario: Memoria

- GIVEN a memoria PDF
- WHEN corpus extract runs
- THEN no `presentacion|*` claim and no EEFF neto from that PDF
