# press-ltm Specification

## Purpose

Extract the comunicado’s stated EBITDA LTM margin as a typed claim so it can be cited independently of the results-presentation highlights.

## Requirements

### Requirement: LTM percentage from press prose

When a press-release parse contains `EBITDA (LTM)` or `EBITDA (últimos 12 meses)` followed by a two-digit percent, extract MUST emit `press_ebitda_margin_ltm` with that digit string and the matching `source_text` and page.

#### Scenario: 1T26 comunicado

- GIVEN MinerU fixture for Comunicado 1T26
- WHEN extract runs
- THEN identity `BYMA|2026-03-31|comunicado|press_ebitda_margin_ltm` MUST have value `76`
- AND `source_page` MUST be 2

#### Scenario: 2T26 comunicado

- GIVEN MinerU fixture for Comunicado 2T26
- WHEN extract runs
- THEN the same metric for period `2026-06-30` MUST have value `75`

### Requirement: Matches presentation gold, does not replace it

Press LTM MUST equal presentation LTM for the same period. Presentation claims MUST remain `scope=presentacion`.

#### Scenario: Cross-document 1T26

- GIVEN both plugins extract
- THEN press `76` MUST equal `presentation_ebitda_margin_ltm` for `2026-03-31`

### Requirement: P&L and bare EBITDA still abstain

Asking for net income or tax “del comunicado” MUST abstain. Asking for EBITDA of the comunicado without margen/LTM/12 meses MUST abstain.

#### Scenario: Net income trap

- GIVEN lookup of resultado neto consolidado del comunicado
- THEN route MUST be abstain
