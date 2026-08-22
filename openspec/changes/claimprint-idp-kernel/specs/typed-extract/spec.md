# typed-extract Specification

## Purpose

Turn a document into a typed schema (or abstain). Domain schemas are plugins; the kernel only classifies, selects a page, fills, and validates.

## Requirements

### Requirement: Filename recipe classification

The system MUST map a filename to a recipe id or `UNKNOWN`. Dedicated EEFF filings (name contains `eeff`, not memoria/comunicado/presentación/transcripción) MUST map to `financial_statement` when that recipe exists. Other sample types MUST NOT be classified as `financial_statement`.

#### Scenario: Dedicated EEFF

- GIVEN `BYMA_-_EEFF_31-03-2026_VF.pdf`
- WHEN classified
- THEN recipe id MUST be `financial_statement`

#### Scenario: Memoria is not a dedicated EEFF

- GIVEN a PDF whose name contains `memoria` and `eeff`
- WHEN classified
- THEN recipe MUST NOT be `financial_statement`

### Requirement: Extract only when recipe allows it

Recipes with `extract: false` MUST NOT produce a filled domain schema. `UNKNOWN` MUST NOT extract.

#### Scenario: Press release

- GIVEN a comunicado PDF
- WHEN extract is requested
- THEN the system MUST return no `FinancialStatement`

### Requirement: Page select then fill FinancialStatement

For `financial_statement`, the system MUST select a PDF page using `page_select_keywords` and fill `FinancialStatement` from that page's `pdftotext -layout` text. Amounts MUST appear on the page (no invented digits). `source_page` MUST be the 1-based PDF page used.

#### Scenario: BYMA 1T26 page 4

- GIVEN `BYMA_-_EEFF_31-03-2026_VF.pdf`
- WHEN extracted
- THEN `period` MUST be `2026-03-31`
- AND `net_income_consolidated` MUST be `21262335`
- AND `net_income_attributable_to_parent` MUST be `21259769`
- AND `prior_period_amount_to_ignore` MUST be `22362983`
- AND `source_page` MUST be `4`

#### Scenario: BYMA 2T26 page 4

- GIVEN `BYMA - EEFF 30-06-2026.pdf`
- WHEN extracted
- THEN `period` MUST be `2026-06-30`
- AND consolidado MUST be `81956525`
- AND controlante MUST be `81946993`

### Requirement: Validation abstain

The system MUST run `reject_financial_statement` before emitting claims. A non-empty reject reason MUST yield no claims.

#### Scenario: Equal amounts

- GIVEN consolidado equals controlante
- WHEN validated
- THEN the system MUST abstain
