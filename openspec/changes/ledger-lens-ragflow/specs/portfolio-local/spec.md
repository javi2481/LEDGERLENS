# Delta for portfolio-local

## ADDED Requirements

### Requirement: Synthetic Spanish financial PDFs

The demo MUST include 3–4 synthetic Spanish financial PDFs covering hechos relevantes, estados financieros, memoria, and operativo. MUST NOT be real BYMA filings.

#### Scenario: Fixture set present and not BYMA

- GIVEN a fresh clone
- WHEN `examples/synthetic/` is listed
- THEN 3–4 Spanish synthetic PDFs SHALL cover hechos, estados, memoria, and operativo (not real BYMA)

### Requirement: README startup and E2E checklist

README MUST cover x86_64, ≥16 GB, Docker ≥24 (not ARM64), Spanish UI, Empty response, Show Quote, synthetic-only, OpenRouter default chat+embed, Ollama fallback (`OLLAMA_HOST=0.0.0.0`), Naive default parser, and E2E: ingest, in-corpus cited Q, out-of-corpus Empty response.

#### Scenario: Operator starts from README

- GIVEN Docker and OpenRouter (Ollama optional fallback) meet prerequisites
- WHEN the operator follows README
- THEN they SHALL open RAGFlow UI on port 80

#### Scenario: E2E in-corpus and out-of-corpus

- GIVEN synthetic PDFs are ingested
- WHEN in-corpus then out-of-corpus checklist questions run
- THEN in-corpus MUST be Spanish with Show Quote; out-of-corpus MUST be Spanish Empty response, no invention
