# Delta for document-parse

## ADDED Requirements

### Requirement: PaddleOCR remote layout parser

Ingested PDFs MUST be parsed by self-hosted PaddleOCR `/layout-parsing` as RAGFlow's remote client. Default MUST be PP-StructureV3 CPU (VL MAY override). From RAGFlow, `PADDLEOCR_API_URL` MUST be `http://paddleocr:8080/layout-parsing`. No AI Studio token. Failed parse MUST be visible; MUST NOT invent text.

#### Scenario: Successful parse via Compose DNS

- GIVEN PaddleOCR on the `ragflow` network and `.env.example` defaults
- WHEN a synthetic PDF is ingested
- THEN RAGFlow MUST call `http://paddleocr:8080/layout-parsing` with PP-StructureV3; URL MUST NOT be localhost or 127.0.0.1

#### Scenario: Parser unavailable

- GIVEN PaddleOCR is down or `/layout-parsing` errors
- WHEN ingest is attempted
- THEN ingest MUST fail visibly and MUST NOT fabricate text
