# typed-extract (delta)

## MODIFIED Requirements

### Requirement: Content recipe classification after parse

The system MUST map parse cover text to a recipe id or `UNKNOWN`. Dedicated EEFF filings MUST map to `financial_statement`. Covers that identify a press release MUST map to `press_release` when that recipe exists. Memorias, decks, and transcripts MUST NOT be `financial_statement` or `press_release`, even if later pages contain P&L labels. Filename MUST NOT be the porter.

#### Scenario: Comunicado cover is press_release

- GIVEN MinerU text whose cover contains a press-release announcement
- WHEN classified
- THEN recipe id MUST be `press_release`

#### Scenario: Memoria cover is unknown for extract plugins

- GIVEN MinerU text whose cover contains `memoria`
- WHEN classified
- THEN recipe MUST NOT be `financial_statement` or `press_release`

#### Scenario: Keywords select a block after type

- GIVEN a `financial_statement` artifact
- WHEN extract runs
- THEN `page_select_keywords` MUST pick a page/block inside the artifact
