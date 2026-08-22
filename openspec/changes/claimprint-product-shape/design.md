# Design: Product shape — one finance IDP

## Technical Approach

Docs and catalog only. No extract/lookup behavior change. Graph overlay files stay on disk until `claimprint-claims-to-rag`.

## Architecture Decisions

| Decision | Choice | Rejected | Why |
|----------|--------|----------|-----|
| Story | One product, two contracts | Kernel=product / RAG=frozen demo | User: end-to-end finance IDP |
| `research/` | Delete | Keep dumps | Pivot diary; git retains history |
| Graph | Keep scripts this change | Delete now | Chat still needs inject until change 2 |
| `legal_contract` | Remove recipe | Keep extract:false stub | No PDFs; multi-domain leftover |
| `page_text.py` | Delete | Keep unused helper | Identity reads MinerU artifacts |

## Data Flow

Unchanged: PDF → MinerU fixtures → classify/extract → claims. RAGFlow still consumes `demo_4` + Graph inject.

## File Changes

| File | Action |
|------|--------|
| `openspec/changes/claimprint-product-shape/` | Create SDD |
| README, handoff, testing, plan-siguiente, openspec README, config.yaml | Rewrite pointers |
| `research/` | Delete |
| agenda vLLM/LinkedIn/branding/naive/descartado | Delete |
| `docs/agenda/README.md` | MinerU runbook only (+ Graph note until change 2) |
| `recipes/legal_contract.json` | Delete |
| `schemas/page_text.py`, `tests/test_page_text.py` | Delete |
| `tests/test_schemas.py` | Drop legal_contract asserts |

## Testing Strategy

| Layer | What |
|-------|------|
| Unit | Catalog without legal_contract |
| Integration | `./scripts/check.sh` |
| E2E | N/A |

## Threat Matrix

N/A — no routing, shell, or process-integration boundary beyond existing `check.sh` / export poppler.

## Migration / Rollout

No runtime migration. Graph inject still required on ≥16 GB until change 2.

## Open Questions

None.
