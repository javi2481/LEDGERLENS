# retrieval-pilot Specification

## Purpose

Measure whether Infinity+RAGFlow retrieve the right PDF page for a question, under keyword, vector, and hybrid weights. Not the identity contract.

## Requirements

### Requirement: Qrels are document and page

Each retrieval case MUST name at least one relevant `{doc, page}` from `docs/archivos_muestra/`. It MUST NOT use `identity_key` as the gold unit.

#### Scenario: EEFF neto page

- GIVEN a question about consolidated net income 1T26 in the EEFF
- THEN the relevant set MUST include `BYMA_-_EEFF_31-03-2026_VF.pdf` page 4

### Requirement: Three arms without rerank

The bench MUST record rankings for vector similarity weight `0`, `1`, and `0.3` with rerank off.

#### Scenario: Skip without stack

- GIVEN RAGFlow is unreachable
- WHEN `retrieval_bench.py` runs
- THEN it MUST exit 0 and report skip reason `no_ragflow`

### Requirement: Metrics are exact set membership

`recall_at_k` MUST be 1 if any gold pair appears in the first k hits, else 0. `mrr` MUST be the reciprocal of the first gold rank, or 0.
