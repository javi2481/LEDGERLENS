# claim-inject Specification

## Purpose

Push typed kernel claims into RAGFlow so the chat can cite the EEFF PDF. Must not treat overlay JSON as identity gold.

## ADDED Requirements

### Requirement: Claims are the inject source

The inject MUST read claims from the kernel store or `extract_claims_from_dir`. It MUST NOT read `docs/hechos_eeff.json` or Docling Graph fichas.

#### Scenario: EEFF chunk from claims

- GIVEN claims for period `2026-03-31` with consolidado `21262335` and controlante `21259769`
- WHEN an inject chunk is built for the dedicated 1T26 EEFF
- THEN the chunk MUST include both amounts
- AND the marker MUST be `Ficha IDP`
- AND the chunk MUST NOT tell the model to cite a sidecar `.md`

### Requirement: Dedicated EEFF only

Manual chunks MUST attach only to dedicated financial-statement documents. Comunicados, memorias, decks, and transcripts MUST NOT receive an identity chunk. The assistant prompt MAY list press (and later presentation) claims.

#### Scenario: Skip non-EEFF docs

- GIVEN a dataset with an EEFF PDF and a comunicado PDF
- WHEN inject runs
- THEN a chunk MUST be added only for the EEFF document

### Requirement: Idempotent replace of Graph overlay

A push MUST delete existing chunks whose text contains `Ficha Graph EEFF` or `Ficha IDP` before inserting the new chunk. Prompt upsert MUST replace both Graph and IDP wrapped blocks.

#### Scenario: Second push

- GIVEN a document that already has a Graph or IDP ficha chunk
- WHEN inject runs again
- THEN the old marked chunks MUST be deleted
- AND exactly one new IDP chunk MUST be added
