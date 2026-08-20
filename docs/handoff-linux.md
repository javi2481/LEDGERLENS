# Handoff — retomar

Repo: `https://github.com/javi2481/LEDGERLENS` · rama **`main`**. Engram: proyecto **`ledgerlens`**.

Abrí este archivo primero. Hay **dos rieles**. El clone **no** trae volúmenes Docker ni chunks de `demo_4`.

## Quick path

1. Producto (kernel IDP): `uv venv && uv pip install -r requirements-dev.txt` → `./scripts/check.sh` → `python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"`.
2. OpenSpec activo: [`openspec/changes/ledgerlens-idp-kernel/`](../openspec/changes/ledgerlens-idp-kernel/).
3. Demo RAG: solo si hay ≥16 GB + Docker. **No** `up.sh` en el Linux de ~7 GB.

## Máquina

| Host | Qué hacer |
|------|-----------|
| Linux ~7 GB | Kernel + docs. **No** Compose. |
| Linux ≥16 GB + Docker | Kernel, y si hace falta el demo: `./scripts/up.sh` + MinerU + `push_hechos.py`. |

No commitear `.env`. Overlay Graph **no** va en `up.sh`. No reparsear MinerU para “arreglar” identidad: el contrato IDP es `pdftotext` + pytest.

## Oro (no fusionar)

| Riel | Dónde |
|------|--------|
| Contrato IDP | `recipes/financial_statement.json` + `evals/identity_v1.json` |
| Overlay del chat | `docs/hechos_eeff.json` |

Cifras 1T26/2T26: consolidado `21262335` / `81956525`; controlante `21259769` / `81946993`; página 4.

## Qué no reabrir

- Graph vs Knowledge Graph de RAGFlow: cerrado.
- Gancho nativo Graph (`docs/agenda/graph-nativo.md`): diferido del **demo**, no el siguiente paso de producto.
- Inflar `openspec/changes/ledger-lens-ragflow/`: está congelado como pin.

## Arranque

```bash
git clone https://github.com/javi2481/LEDGERLENS.git
cd LEDGERLENS
git pull origin main
```

En Cursor: Engram `mem_context` con proyecto `ledgerlens`. OpenSpec: `openspec/README.md`.
