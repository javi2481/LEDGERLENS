# product-narrative Specification

## Purpose

Living product docs MUST describe LedgerLens as one finance IDP: MinerU parse, typed identity, RAGFlow UI. Pivot rails and unused catalog stubs MUST NOT appear as current product.

## ADDED Requirements

### Requirement: One product story

README, OpenSpec README, handoff, and `openspec/config.yaml` context MUST name this change as the active product change. They MUST describe RAGFlow as the product UI (pinned stack), not as a disposable demo rail. Identity SoT MUST remain `evals/` + recipes. Chat overlay gold MUST NOT be described as the identity contract.

#### Scenario: Active change pointer

- GIVEN `README.md` and `openspec/README.md`
- WHEN a reader looks for the open product change
- THEN both MUST name `ledgerlens-product-shape`
- AND `ledgerlens-mineru-parse` MUST be listed as shipped, not activo
- AND `ledger-lens-ragflow` MUST remain the UI/stack pin (do not inflate)

### Requirement: Finance catalog only

The recipe catalog MUST NOT include `legal_contract`. `annual_report` and `earnings_transcript` MAY remain with `extract: false`. Identity extract MUST NOT call `pdftotext` via `schemas/page_text.py`.

#### Scenario: Catalog load

- GIVEN `recipes/` after this change
- WHEN `load_recipes()` runs
- THEN recipe ids MUST NOT include `legal_contract`
- AND `financial_statement` and `press_release` MUST still extract

#### Scenario: No identity pdftotext module

- GIVEN the kernel tree
- WHEN identity extract runs
- THEN text MUST come from `schemas.parse_artifact.page_text`
- AND `schemas/page_text.py` MUST NOT exist
