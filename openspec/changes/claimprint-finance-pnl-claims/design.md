# Design: Finance P&L neighbor claims

## Technical Approach

Keep `FinancialStatement` as the two-row gate. Add a finance-only line catalog. Extract the same `pdftotext` page 4. First amount column is the period figure (2T26 YTD). Parentheses mean negative.

## Architecture Decisions

| Decision | Choice | Rejected | Why |
|----------|--------|----------|-----|
| Schema | Line catalog + extra claims | Six new DTO fields | Kernel Claim stays generic |
| 2T26 column | First amount | Three-month columns | Matches existing neto gold |
| no controlante | Own metric | Negation of controlante → neto | Current lookup would pick 21262335 |
| Gold | Recipe JSON | hechos_eeff.json | Overlay is demo-only |

## Data Flow

```
page text → FinancialStatement + reject
         → line matchers → extra Claims
question → metric + scope + period → filter claims
```

## Testing Strategy

identity_v1 regression. identity_v2 for neighbor rows. Amounts must appear on the page (digits; sign is parser-side).

## Threat Matrix

No new subprocess. `pdftotext` argv list unchanged.

## Migration

No demo migration. Overlay Graph still two net rows.
