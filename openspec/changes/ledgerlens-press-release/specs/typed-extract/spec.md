# typed-extract (delta)

## MODIFIED Requirements

### Requirement: Filename recipe classification

The system MUST map a filename to a recipe id or `UNKNOWN`. Dedicated EEFF filings MUST map to `financial_statement`. Filenames containing `comunicado` MUST map to `press_release` when that recipe exists. Memorias, decks, and transcripts MUST NOT be `financial_statement` or `press_release`.

#### Scenario: Comunicado is press_release

- GIVEN `BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf`
- WHEN classified
- THEN recipe id MUST be `press_release`

#### Scenario: Memoria is still unknown for extract plugins

- GIVEN a PDF whose name contains `memoria`
- WHEN classified
- THEN recipe MUST NOT be `financial_statement` or `press_release`
