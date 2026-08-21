# Tasks: Press-release EBITDA LTM

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~150–250 authored |
| 400-line budget risk | Low |
| Delivery strategy | single-pr |

### Suggested Work Units

| Unit | Goal | Focused test |
|------|------|--------------|
| A | Extract + recipe gold | `pytest tests/test_press_release.py` |
| B | Lookup + press_v1 evals | `pytest tests/test_evals_press.py tests/test_lookup.py` |
| C | Docs + HITL example keys | `./scripts/check.sh` |

- [x] 1.1 Metric, extract scan, claims
- [x] 1.2 Lookup route; evals; cross-check vs deck
- [x] 1.3 Docs + example verdicts
