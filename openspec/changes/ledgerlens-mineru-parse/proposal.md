# Proposal: MinerU parse as the only identity path

> **Change activo (producto).** No inflar [`ledgerlens-idp-kernel`](../ledgerlens-idp-kernel/), [`ledgerlens-finance-pnl-claims`](../ledgerlens-finance-pnl-claims/), [`ledgerlens-claim-store`](../ledgerlens-claim-store/), [`ledgerlens-press-release`](../ledgerlens-press-release/), ni el pin [`ledger-lens-ragflow`](../ledger-lens-ragflow/).

## Intent

Identity today classifies by filename and extracts with `pdftotext`. The demo already parsed the same PDFs with MinerU. Claimprint MUST use that parse as the only text path: ingest → MinerU artifact → classify by cover → extract typed claims. RAG remains narrative, not identity SoT (Unify: one FileManager parse, typed Knowledge, no stuffing rows back into recoverable chunks).

## Scope

### In Scope

- Versioned `fixtures/mineru/*.md` per sample PDF
- Export script from RAGFlow `demo_4` chunks (demo host); no live MinerU in `check.sh`
- Classify from cover text (not filename); memoria/deck/transcript stay `UNKNOWN`
- Extract EEFF and press from the same artifact; claim-store fingerprint includes parse hash
- Docs: one parser, two consumers (claims + RAG)

### Out of Scope

Reparse MinerU, PaddleOCR/Docling classifiers, LLM type, Postgres, Graph overlay as SoT, inflating the RAGFlow pin, `app.py`

## Capabilities

### New Capabilities

- `parse-artifact`: Durable MinerU markdown is the parse SoT. Missing artifact MUST NOT fall back to `pdftotext`.

### Modified Capabilities

- `typed-extract`: Classify after parse (cover window). Keywords select a block in the artifact, not a `pdftotext` page.

## Approach

Materialize MinerU text. Kernel reads fixtures. Evals stay exact-match gold in recipes. Overlay `hechos_eeff.json` stays demo-only.

## Rollback Plan

Revert this change folder, `schemas/parse_artifact.py`, classify/extract/corpus/store wiring, fixtures, export script, docs. Previous filename+`pdftotext` path returns only via revert, not a silent fallback.

## Success Criteria

- [x] EEFF 1T26/2T26 gold still matches without `pdftotext` in extract
- [x] Comunicado dates still match; memoria does not yield P&L claims
- [x] `check.sh` does not require `pdftotext` as identity parser
- [x] `ledger-lens-ragflow` unchanged
