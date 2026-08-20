# claim-store Specification

## Purpose

Serve typed claims to identity lookup from a local JSON cache so a second question does not re-parse unchanged PDFs. Extract remains the source of truth when the cache is missing, stale, corrupt, or force-refreshed.

## Requirements

### Requirement: Cache hit skips extract

When the store file exists, is valid, and the PDF fingerprint matches the directory, `load_claims` MUST return the stored claims and MUST NOT call extract.

#### Scenario: Second load

- GIVEN a directory of PDFs and a store written from a first extract
- WHEN `load_claims` runs again without `force`
- THEN extract MUST NOT be called
- AND the claims MUST equal the first result

### Requirement: Miss, stale, or force re-extracts

The store MUST call extract and rewrite the file when the store is missing, the fingerprint does not match, the JSON is corrupt, or `force` is true.

#### Scenario: PDF mtime changed

- GIVEN a fresh store
- WHEN a PDF size or mtime changes
- THEN extract MUST run and the store MUST be rewritten

#### Scenario: Refresh flag

- GIVEN a fresh store
- WHEN `force` is true
- THEN extract MUST run even if the fingerprint matches

### Requirement: CLI uses the store; evals do not

`idp_ask.py` MUST load claims via the store. Identity eval harnesses MUST keep calling `extract_claims_from_dir` so gold does not depend on `outputs/`.

#### Scenario: Eval isolation

- GIVEN `evals/identity_v1.json` and `identity_v2.json`
- WHEN pytest runs those harnesses
- THEN they MUST NOT read `outputs/claims.json`

### Requirement: Cache is local and not SoT overlay

The store MUST live under `outputs/` (gitignored). It MUST NOT write `docs/hechos_eeff.json` or touch Compose / RAGFlow.

#### Scenario: Overlay untouched

- GIVEN a CLI ask that writes the store
- THEN `docs/hechos_eeff.json` MUST be unchanged
