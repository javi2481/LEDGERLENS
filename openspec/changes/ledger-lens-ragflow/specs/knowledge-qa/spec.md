# Delta for knowledge-qa

## ADDED Requirements

### Requirement: Spanish cited answers

Q&A MUST be RAGFlow knowledge-base chat. Non-empty answers MUST be Spanish and MUST cite evidence via Show Quote.

#### Scenario: Evidence-backed Spanish answer

- GIVEN parsed BYMA PDFs in `demo_4` contain a known fact
- WHEN the user asks a Spanish question those PDFs answer
- THEN the reply MUST be Spanish with Show Quote; uncited non-empty answers MUST NOT be shown

### Requirement: No-evidence empty response

Missing or low-similarity evidence MUST yield the configured Spanish Empty response. MUST NOT invent facts or citations. Empty response MUST NOT be blank.

#### Scenario: No matching or weak chunks

- GIVEN no relevant content or only low-similarity chunks
- WHEN the user asks a question
- THEN it MUST return the Spanish no-evidence Empty response without invention

#### Scenario: Blank Empty response forbidden

- GIVEN a LedgerLens demo chat assistant
- WHEN Empty response is inspected
- THEN it MUST be a Spanish no-evidence sentence and MUST NOT be blank
