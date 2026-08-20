# Handoff — retomar en otra PC

Repo: `https://github.com/javi2481/LEDGERLENS` · rama **`main`**. Engram: proyecto **`ledgerlens`**.

Abrí este archivo primero. Hay **dos rieles**. El clone **no** trae volúmenes Docker ni chunks de `demo_4`. Código de producto (kernel + P&L) **ya está en GitHub** (`f63d954`).

## Quick path

```bash
git pull origin main
uv venv && uv pip install -r requirements-dev.txt
./scripts/check.sh
python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"
# → 21262335
python scripts/idp_ask.py "¿Cuál es el resultado bruto del 1T26?"
# → 60144176
```

Siguiente slice de producto (después de este cache): segundo dominio, ver [plan-siguiente-idp.md](plan-siguiente-idp.md).

OpenSpec: activo [`ledgerlens-claim-store`](../openspec/changes/ledgerlens-claim-store/). Kernel shipped [`ledgerlens-idp-kernel`](../openspec/changes/ledgerlens-idp-kernel/). P&L vecino shipped [`ledgerlens-finance-pnl-claims`](../openspec/changes/ledgerlens-finance-pnl-claims/). Pin demo congelado [`ledger-lens-ragflow`](../openspec/changes/ledger-lens-ragflow/).

## Máquina

| Host | Qué hacer |
|------|-----------|
| Linux ~7 GB | Kernel + docs. **No** Compose. |
| Linux ≥16 GB + Docker | Kernel, y si hace falta el demo: `./scripts/up.sh` + MinerU + `push_hechos.py`. |

No commitear `.env`. Overlay Graph **no** va en `up.sh`. No reparsear MinerU para “arreglar” identidad: el contrato IDP es `pdftotext` + pytest.

## Hecho (no reabrir)

| Slice | Commit | Qué es |
|-------|--------|--------|
| Kernel extract + lookup | `b6cb24a` | capa 1–2, `evals/identity_v1.json`, `idp_ask.py` |
| Dos rieles (docs) | `ef40b24` | producto IDP vs demo RAGFlow |
| P&L vecino extract | `26c67de` | bruto / operativo / EBT / impuesto / no controlante |
| P&L vecino lookup + v2 | `f63d954` | `evals/identity_v2.json` |

SDD hybrid. Finanzas es el primer plugin. `FinancialStatement` sigue de portero de los dos netos; las vecinas salen de `schemas/finance_lines.py`.

## Oro (no fusionar)

| Riel | Dónde |
|------|--------|
| Contrato IDP | `recipes/financial_statement.json` + `evals/identity_v1.json` + `evals/identity_v2.json` |
| Overlay del chat | `docs/hechos_eeff.json` (`push_hechos.py`) |

1T26: neto `21262335`, controlante `21259769`, bruto `60144176`, operativo `70223471`, impuesto `-14950948`, no controlante `2566`. Página 4. 2T26: primera columna (YTD).

## Qué falta (producto)

Orden fijo. Un change OpenSpec **nuevo** por slice. No inflar el kernel ni el pin RAGFlow.

1. **Persistir claims** (activo: [`ledgerlens-claim-store`](../openspec/changes/ledgerlens-claim-store/)). JSON en `outputs/claims.json`. `idp_ask.py` reusa el cache; `--refresh` reextrae. Pytest de evals sigue extrayendo.
2. **Segundo dominio.** Una receta + un schema + pocos gold. Prueba que el kernel no es solo BYMA.

No ahora: capa 3 RAG, MinerU en CI, ingresos/EPS, gancho Graph, Compose, `app.py` / `ledger_lens/`.

## Qué no reabrir

- Graph vs Knowledge Graph de RAGFlow.
- Gancho nativo Graph (`docs/agenda/graph-nativo.md`): diferido del **demo**.
- Inflar `openspec/changes/ledger-lens-ragflow/`.
- Tratar el overlay Graph como contrato IDP.

## Arranque

```bash
git clone https://github.com/javi2481/LEDGERLENS.git
cd LEDGERLENS
git pull origin main
```

En Cursor: Engram `mem_context` con proyecto `ledgerlens`. OpenSpec: `openspec/README.md`.
