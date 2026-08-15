# Delta for document-parse

## ADDED Requirements

### Requirement: Docling default PDF parser for BYMA filings

Ingested demo PDFs MUST use RAGFlow **Docling** (classic layout + TableFormer via sidecar `DOCLING_SERVER_URL`). Corpus lives in `docs/archivos_muestra/`. Failed parse MUST be visible; MUST NOT invent text. Naive MAY be selected if Docling Serve is down. DeepDoc MAY be selected if a PDF has no text layer. PaddleOCR MUST NOT be required for the default demo. Granite-Docling VLM MUST NOT be the default parser.

#### Scenario: Default ingest uses Docling

- GIVEN `.env.example` defaults (`COMPOSE_PROFILES=infinity,cpu`, `DOCLING_SERVER_URL=http://docling-serve:5001`, `USE_DOCLING=false`, PaddleOCR vars commented)
- WHEN a BYMA PDF is ingested with the dataset PDF parser set to Docling
- THEN RAGFlow MUST call Docling Serve and MUST NOT require `paddleocr`, DeepDoc OCR, or in-process `USE_DOCLING=true`

### Requirement: Optional PaddleOCR remote layout parser

PaddleOCR MAY be enabled as an alternate PDF parser: Compose profile `paddleocr`, `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`, algorithm PP-StructureV3 CPU (VL MAY override). No AI Studio token. From RAGFlow the URL MUST NOT be localhost or 127.0.0.1. Failed parse MUST be visible; MUST NOT invent text.

#### Scenario: Optional parse via Compose DNS

- GIVEN profile `paddleocr` is enabled and PaddleOCR env vars are uncommented
- WHEN a synthetic PDF is ingested with dataset PDF parser = PaddleOCR
- THEN RAGFlow MUST call `http://paddleocr:8080/layout-parsing` with PP-StructureV3

#### Scenario: Parser unavailable

- GIVEN the selected parser (Docling, Naive, DeepDoc, or PaddleOCR) is down or errors
- WHEN ingest is attempted
- THEN ingest MUST fail visibly and MUST NOT fabricate text
