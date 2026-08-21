# Proposal: Results-presentation identity plugin

> **Change activo (producto).** No inflar kernel, P&L, press, mineru-parse, product-shape, claims-to-rag, ni el pin RAGFlow.

## Intent

Decks still skip extract. LedgerLens MUST add a third finance plugin: EBITDA + LTM margin from highlights — not slide-2 P&L (millions, inflation view, 2T26 quarterly vs EEFF YTD).

## Scope

### In Scope

- Cover `presentación de resultados` → `results_presentation`
- Extract `presentation_ebitda` + `presentation_ebitda_margin_ltm`; period for identity_key
- Gold 1T26/2T26; `evals/presentation_v1.json`; v1/v2/press still abstain on EEFF metrics “de la presentación” and P&L “de la memoria”
- Corpus dispatch; inject already lists all claims

### Out of Scope

Slide-2 P&L, AUC, segment split, presentation as-of date (duplicates press), transcript plugin, other domains, inflating shipped changes / pin

## Capabilities

### New Capabilities

- `presentation-extract`: Highlights EBITDA + LTM margin only.
- `presentation-lookup`: EBITDA/margen de la presentación; EEFF+deck and memoria+P&L abstain.
- `presentation-evals`: exact-match; prior evals green.

### Modified Capabilities

- `typed-extract`: Deck cover is `results_presentation`. Memorias/transcripts stay UNKNOWN. No FinancialStatement from a deck or memoria.

## Approach

`schemas/results_presentation.py` after press-release. Flip recipe `extract: true`. Remove deck from `COVER_SKIP`. Lookup presentation intent before narrative `presentacion de resultados`.

## Rollback Plan

Revert this folder, plugin, recipe gold, classify, corpus, lookup, evals. Finance/press/inject stay.

## Success Criteria

- [ ] 1T26 EBITDA `72128`; LTM `76`; period `2026-03-31`
- [ ] 2T26 EBITDA `71697`; LTM `75`; period `2026-06-30`
- [ ] Neto/impuesto de la presentación and neto de la memoria abstain
- [ ] identity_v1, identity_v2, press_v1 green
