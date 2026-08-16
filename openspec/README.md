# OpenSpec / Gentle AI (hybrid)

LedgerLens usa SDD **hybrid**: archivos en `openspec/` + observaciones Engram (`project: ledgerlens`).

## Quick path

1. Change activo: [`changes/ledger-lens-ragflow/`](changes/ledger-lens-ragflow/).
2. E2E Windows 32 GB cerrado (BYMA 1T26). No reabrir compose en el Linux de ~7 GB ([descartado](../docs/agenda/descartado.md)).

## Details

| Tema | Valor |
|------|--------|
| Producto | Q&A español + citas; empty response si no hay evidencia |
| Stack en config | MinerU `pipeline` + Infinity + Gemini chat + Voyage nativo; Ollama último fallback; PaddleOCR opcional |
| Tests | `./scripts/check.sh` (no Strict TDD; E2E manual en ≥16 GB) |
| Persistencia | `openspec/config.yaml` → `persistence: hybrid` |

## Checklist

- [ ] Specs/design/README describen el **mismo** default (MinerU pipeline, Gemini, Voyage, Infinity)
- [ ] `.env` y API keys **no** están en git

## Next step

En la PC potente: `./scripts/up.sh` + checklist E2E del README raíz. Después, verify SDD y archive del change `ledger-lens-ragflow`.
