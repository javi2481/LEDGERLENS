# Design: Claimprint IDP kernel (extract + identity)

## Technical Approach

Add a domain-agnostic kernel beside the RAGFlow demo: classify → page text → plugin schema → claims → lexical lookup. Finance is the only plugin in this slice (`FinancialStatement`). CI uses `pdftotext`, not MinerU or Docling Graph. Overlay scripts stay the demo adapter, not the source of truth.

## Architecture Decisions

| Decision | Choice | Rejected | Why |
|----------|--------|----------|-----|
| Parser for evals | `pdftotext -layout` | MinerU sidecar; Docling Graph | Runs on ~7 GB; no Docker. Graph stays overlay-only. |
| Package layout | `schemas/` + `evals/` + `scripts/` | `ledger_lens/`, `app.py` | OpenSpec demo forbid list; this is not a RAG package. |
| Query understanding | Lexical rules first | LLM judge / embeddings | Exact-match gold; LLM only if rules miss (not in this slice). |
| Catalog constraint | ≥1 recipe | Require `financial_statement` | Kernel must not hard-code finance. |
| Persistence | In-memory claims from extract | Postgres / JSON SoT overwrite of `hechos_eeff.json` | First slice is eval/harness. |
| Default identity | consolidado if unspecified | Always ask user | Matches existing `GRAPH_RULES` product policy. |

## Data Flow

```
PDF filename → recipe | UNKNOWN
     extract:true → page_select_keywords → pdftotext page
     → FinancialStatement → reject_* → two Claims
Question → route identity|abstain|narrative
     identity → filter claims by scope/period → evidence
     narrative → skip (capa 3)
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `openspec/changes/claimprint-idp-kernel/` | Create | SDD artifacts |
| `schemas/claim.py` | Create | Claim + identity_key |
| `schemas/classify.py` | Create | Filename → recipe; dedicated EEFF heuristic |
| `schemas/page_text.py` | Create | pdftotext helper (argv list, no shell) |
| `schemas/extract.py` | Create | Page select + FinancialStatement fill |
| `schemas/lookup.py` | Create | Lexical intent + lookup |
| `schemas/catalog.py` | Modify | Do not require `financial_statement` |
| `schemas/__init__.py` | Modify | Export kernel types |
| `scripts/graph_hechos.py` | Modify | `needs_graph` delegates to classify |
| `scripts/idp_ask.py` | Create | CLI question → lookup |
| `evals/identity_v1.json` | Create | Structured cases |
| `tests/test_extract.py` | Create | Layer 1 |
| `tests/test_lookup.py` | Create | Layer 2 |
| `tests/test_evals_file.py` | Create | Gold file contract |
| `pytest.ini` | Create | `pythonpath = .` |
| `scripts/check.sh` | Modify | Run pytest |
| `README.md`, `docs/testing.md` | Modify | Rumbo + eval contract |

## Interfaces / Contracts

```text
Claim: identity_key, value, period, source_page, source_text, issuer, scope, metric
LookupResult: route, claims, abstain_reason, compare
pdftotext: subprocess.run(["pdftotext", "-layout", "-f", N, "-l", N, pdf, "-"])
```

## Testing Strategy

| Layer | What | Approach |
|-------|------|----------|
| Unit | classify, intent, identity_key, reject | pytest, no PDF |
| Integration | 1T26/2T26 pdftotext extract vs recipe gold | pytest + poppler |
| Eval | identity_v1.json harness | exact match; narrative skip |
| E2E RAG | unchanged | still manual on ≥16 GB |

## Threat Matrix

`pdftotext` is an explicit subprocess. No shell interpolation.

| Boundary | Applicability | Design response | Planned RED tests |
|----------|---------------|-----------------|-------------------|
| Shell / subprocess | Applicable: argv list to `pdftotext` | `subprocess.run` sequence only; `shell=False`; Path as argument | test refuses to build a shell string from filename |
| Documentation-like paths | N/A | — | none |
| Git / PR / push | N/A | — | none |

## Migration / Rollout

No migration. Demo volumes untouched. Rollback: git revert this change.

## Open Questions

- [x] LLM extract fallback — deferred; rules on page 4 are sufficient for gold.
