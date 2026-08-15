# Delta for portfolio-local

## ADDED Requirements

### Requirement: BYMA sample financial PDFs

The demo MUST include BYMA sample PDFs covering comunicados, EEFF, presentaciones, and memoria in `docs/archivos_muestra/`.

#### Scenario: Fixture set present

- GIVEN a fresh clone
- WHEN `docs/archivos_muestra/` is listed
- THEN Spanish BYMA PDFs SHALL cover comunicado, EEFF, and presentación

### Requirement: README startup and E2E checklist

README MUST cover x86_64, ≥16 GB, Docker ≥24 (not ARM64), Spanish UI, Empty response, Show Quote, BYMA samples in `docs/archivos_muestra/`, OpenRouter default chat, Voyage embed, Ollama fallback (`OLLAMA_HOST=0.0.0.0`), Docling default parser, and E2E: ingest, in-corpus cited Q, out-of-corpus Empty response.

#### Scenario: Operator starts from README

- GIVEN Docker and OpenRouter (Ollama optional fallback) meet prerequisites
- WHEN the operator follows README
- THEN they SHALL open RAGFlow UI on port 80

#### Scenario: E2E in-corpus and out-of-corpus

- GIVEN BYMA PDFs are ingested
- WHEN in-corpus then out-of-corpus checklist questions run
- THEN in-corpus MUST be Spanish with Show Quote; out-of-corpus MUST be Spanish Empty response, no invention
