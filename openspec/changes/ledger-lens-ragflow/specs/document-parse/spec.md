# Delta for document-parse

## ADDED Requirements

### Requirement: Naive default PDF parser for synthetic fixtures

Ingested demo PDFs MUST use RAGFlow **Naive** by default (skip OCR/TSR/DLR). Fixtures in `examples/synthetic/` MUST have an extractable text layer. Failed parse MUST be visible; MUST NOT invent text. DeepDoc MAY be selected if a PDF has no text layer. PaddleOCR MUST NOT be required for the default demo.

#### Scenario: Default ingest uses Naive

- GIVEN `.env.example` defaults (`COMPOSE_PROFILES=infinity,cpu`, PaddleOCR vars commented)
- WHEN a synthetic PDF is ingested with the dataset PDF parser set to Naive
- THEN RAGFlow MUST parse via Naive and MUST NOT require `paddleocr` or DeepDoc OCR

### Requirement: Optional PaddleOCR remote layout parser

PaddleOCR MAY be enabled as an alternate PDF parser: Compose profile `paddleocr`, `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`, algorithm PP-StructureV3 CPU (VL MAY override). No AI Studio token. From RAGFlow the URL MUST NOT be localhost or 127.0.0.1. Failed parse MUST be visible; MUST NOT invent text.

#### Scenario: Optional parse via Compose DNS

- GIVEN profile `paddleocr` is enabled and PaddleOCR env vars are uncommented
- WHEN a synthetic PDF is ingested with dataset PDF parser = PaddleOCR
- THEN RAGFlow MUST call `http://paddleocr:8080/layout-parsing` with PP-StructureV3

#### Scenario: Parser unavailable

- GIVEN the selected parser (Naive, DeepDoc, or PaddleOCR) is down or errors
- WHEN ingest is attempted
- THEN ingest MUST fail visibly and MUST NOT fabricate text
