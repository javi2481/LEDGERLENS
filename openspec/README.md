# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Change activo: [`changes/ledger-lens-ragflow/`](changes/ledger-lens-ragflow/).
2. No archivar hasta el E2E en un host ≥16 GB ([docs/agenda/e2e-16gb.md](../docs/agenda/e2e-16gb.md)).
3. Ignorar [`changes/ledger-lens-mvp/`](changes/ledger-lens-mvp/) (Gradio / HF Space; el producto se vació).

## Details

| Tema | Valor |
|------|--------|
| Producto | Q&A español + citas; empty response si no hay evidencia |
| Stack en config | Naive + Infinity + OpenRouter; Ollama fallback; PaddleOCR opcional |
| Tests | `./scripts/check.sh` (no Strict TDD; E2E manual en ≥16 GB) |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] Specs/design/README describen el **mismo** default (Naive, OpenRouter, Infinity)
- [ ] `.env` y API keys **no** están en git
- [ ] `ledger-lens-mvp` no se trata como el producto actual

## Next step

En la PC potente: `./scripts/up.sh` + checklist E2E del README raíz. Después, verify SDD y archive del change `ledger-lens-ragflow`.
