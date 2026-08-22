# typed-extract (delta)

## MODIFIED Requirements

### Requirement: Content recipe classification after parse

The system MUST map parse cover text to a recipe id or `UNKNOWN`. Dedicated EEFF filings MUST map to `financial_statement`. Press-release covers MUST map to `press_release` when that recipe exists. Covers that identify a results presentation MUST map to `results_presentation` when that recipe exists. Memorias and transcripts MUST NOT be `financial_statement`, `press_release`, or `results_presentation`, even if later pages contain P&L labels. Filename MUST NOT be the porter.

(Previously: decks were forced to `UNKNOWN` via cover skip.)

#### Scenario: Deck cover is results_presentation

- GIVEN MinerU text whose cover contains `Presentación de Resultados`
- WHEN classified
- THEN recipe id MUST be `results_presentation`

#### Scenario: Memoria cover is unknown for extract plugins

- GIVEN MinerU text whose cover contains `memoria`
- WHEN classified
- THEN recipe MUST NOT be `financial_statement`, `press_release`, or `results_presentation`

#### Scenario: Transcript cover is unknown

- GIVEN an earnings-transcript cover
- WHEN classified
- THEN recipe MUST NOT be `financial_statement`, `press_release`, or `results_presentation`

#### Scenario: Keywords select a block after type

- GIVEN a `results_presentation` artifact
- WHEN extract runs
- THEN `page_select_keywords` MUST pick the highlights block inside the artifact
