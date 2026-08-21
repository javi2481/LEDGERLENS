# parse-artifact

## Requirements

### Requirement: Durable MinerU text is the parse source of truth

The system MUST load document text for classify and extract from `fixtures/mineru/<pdf-stem>.md`. The system MUST NOT call `pdftotext` or MinerU HTTP from identity extract. If the artifact is missing, extract MUST return no row (treat as unclassified).

#### Scenario: Extract uses the artifact

- GIVEN `fixtures/mineru/BYMA_-_EEFF_31-03-2026_VF.md` exists
- WHEN `extract_financial_statement` runs on that PDF
- THEN the text MUST come from the artifact, not a poppler subprocess

#### Scenario: Missing artifact does not fall back

- GIVEN a PDF with no matching `fixtures/mineru/*.md`
- WHEN extract runs
- THEN the result MUST be empty, not a `pdftotext` parse
