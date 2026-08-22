# Proposal: Academic close (HITL, dossier, orientation probe)

> **Shipped.** No inflar. El change activo es [`claimprint-rag-pilot`](../claimprint-rag-pilot/).

## Intent

The finance IDP extracts typed claims and feeds RAGFlow, but the academic plant still lacks a human review pack, a citable Q&A export, and a document-orientation preprocess probe. Claimprint MUST close the MVP with those three pieces plus docs for Infinity hybrid retrieval — without a second BM25 library, custom UI, or new extract plugins.

## Scope

### In Scope

- Assisted HITL: verdicts `accept` / `reject` / `flag` keyed by `identity_key`; default all-accept
- HTML review pack + example verdicts JSON
- HTML dossier: facts by period, gold identity Q&A, abstentions, HITL annex
- Optional Paddle orientation probe (cover page); skip without Paddle
- Docs: two machines, hybrid keyword+vector on Infinity, desktop checklist
- `check.sh` contracts for new scripts; pytest without Docker/Paddle

### Out of Scope

Transcript/annual extract, custom UI, ML confidence, UVDoc, Whoosh/Okapi BM25, ERP/API, inflating `push_claims.py`, recreating `research/`, editing vendor pin

## Capabilities

### New Capabilities

- `hitl-review`: Verdicts over claims; missing file means accept-all.
- `academic-dossier`: HTML of accepted facts + gold identity Q&A + abstain + HITL annex.
- `preprocess-orientation`: Optional cover-page orientation; CI must skip without Paddle.

### Modified Capabilities

None (recipes stay as they are; memorias/transcripts remain `extract: false`).

## Approach

Pure helpers in `schemas/review.py` and `schemas/dossier.py`. CLIs write gitignored `outputs/`. Example verdicts committed under `examples/`. Preprocess is a desktop script, not a `requirements-dev` dependency.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `schemas/review.py`, `schemas/dossier.py` | New | Verdicts + HTML builders |
| `scripts/review_pack.py`, `informe.py`, `preprocess_probe.py` | New | CLIs |
| `examples/review_verdicts.example.json` | New | All-accept template |
| `tests/test_review.py`, `test_informe.py`, `test_preprocess.py` | New | Unit + skip |
| README, handoff, testing, plan-siguiente, `docs/cierre-academico.md` | Modified/New | Close pointers |
| `scripts/check.sh`, `openspec/config.yaml` | Modified | Contracts + active change |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| CI requires Paddle | Med | Probe exits 0 and skips; not in requirements-dev |
| Empty verdicts break evals | Low | Default accept; evals still extract, ignore HITL |
| Dossier HTML too large | Low | Identity cases only; skip narrative |

## Rollback Plan

Revert this folder, `schemas/review.py`, `schemas/dossier.py`, new scripts/tests/examples, and doc pointers. Kernel, evals, pin, and inject stay.

## Success Criteria

- [ ] `./scripts/check.sh` green on ~7 GB without Paddle
- [ ] Dossier includes 1T26 neto `21262335` page 4 when verdicts default
- [ ] A `reject` claim does not appear in published facts
- [ ] Preprocess without Paddle does not fail CI
- [ ] README names Infinity hybrid retrieval and says it is not the identity contract
