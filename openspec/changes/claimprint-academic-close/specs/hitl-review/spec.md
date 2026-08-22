# hitl-review Specification

## Purpose

Let a human accept, reject, or flag typed claims before they appear as published facts in the academic dossier. Missing verdicts MUST NOT break identity evals or CI.

## Requirements

### Requirement: Default accept when verdicts are absent

When no verdicts file exists, every claim MUST be treated as `accept`.

#### Scenario: Missing file

- GIVEN a set of claims and no verdicts path (or a missing file)
- WHEN publishable claims are computed
- THEN the full claim set MUST be returned
- AND no exception MUST be raised

### Requirement: Reject is unpublished

A claim whose verdict is `reject` MUST NOT appear in the published-facts list.

#### Scenario: One reject

- GIVEN two claims A and B
- AND a verdicts file that sets A to `reject` and omits B
- WHEN publishable claims are computed
- THEN the result MUST contain B and MUST NOT contain A

### Requirement: Flag is annex-only

A `flag` verdict MUST NOT be treated as a published fact. It MUST still be listed for the HITL annex.

#### Scenario: Flagged row

- GIVEN a claim with verdict `flag`
- WHEN publishable claims are computed
- THEN that claim MUST be absent from published facts
- AND it MUST be present in the flagged list

### Requirement: Review pack is not a product UI

`scripts/review_pack.py` MUST write an HTML table of claims with identity_key, value, page, and source_text. It MUST NOT start a web server or replace RAGFlow.

#### Scenario: Pack writes HTML

- GIVEN claims from the kernel
- WHEN the review pack renderer runs
- THEN the HTML MUST include each `identity_key` and `source_text` when present
