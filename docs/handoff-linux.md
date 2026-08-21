# Handoff — retomar en otra PC

Repo: `https://github.com/javi2481/LEDGERLENS` · rama **`main`**. Engram: proyecto **`ledgerlens`**.

Abrí este archivo primero. Hay **un parse MinerU** y dos consumidores (claims tipados vs chat RAG). El clone trae `fixtures/mineru/*.md`; **no** trae volúmenes Docker ni chunks de `demo_4`. Código de producto **ya está en GitHub**.

## Quick path

```bash
git pull origin main
uv venv && uv pip install -r requirements-dev.txt
./scripts/check.sh
python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"
# → 21262335
python scripts/idp_ask.py "¿Cuál es la fecha del comunicado de prensa 1T26?"
# → 2026-05-08
```

Siguiente producto: más identidad **financiera** sobre los mismos PDF (`docs/archivos_muestra/`), p. ej. presentación. Ver [plan-siguiente-idp.md](plan-siguiente-idp.md). No otros dominios.

OpenSpec: activo [`ledgerlens-mineru-parse`](../openspec/changes/ledgerlens-mineru-parse/). Shipped: kernel, P&L, [`ledgerlens-claim-store`](../openspec/changes/ledgerlens-claim-store/), [`ledgerlens-press-release`](../openspec/changes/ledgerlens-press-release/). Pin demo congelado [`ledger-lens-ragflow`](../openspec/changes/ledger-lens-ragflow/).

## Máquina

| Host | Qué hacer |
|------|-----------|
| Linux ~7 GB | Kernel + docs. **No** Compose. |
| Linux ≥16 GB + Docker | Kernel, y si hace falta el demo: `./scripts/up.sh` + MinerU + `push_hechos.py`. |

No commitear `.env`. Overlay Graph **no** va en `up.sh`. No reparsear MinerU para “arreglar” identidad: el contrato IDP es `fixtures/mineru/` + pytest. En la PC del demo: `python scripts/export_mineru.py` pisa los artefactos con los chunks de `demo_4`.

## Hecho (no reabrir)

| Slice | Commit | Qué es |
|-------|--------|--------|
| Kernel extract + lookup | `b6cb24a` | capa 1–2, `evals/identity_v1.json`, `idp_ask.py` |
| Dos rieles (docs) | `ef40b24` | producto IDP vs demo RAGFlow |
| P&L vecino extract | `26c67de` | bruto / operativo / EBT / impuesto / no controlante |
| P&L vecino lookup + v2 | `f63d954` | `evals/identity_v2.json` |
| Cache CLI de claims | `48e9091` | `outputs/claims.json`; evals siguen extrayendo |
| Un parse MinerU | `b13f97f` | `fixtures/mineru/`; clasificar portada; no `pdftotext` de identidad |

SDD hybrid. Dominio único: finanzas BYMA. `FinancialStatement` es el portero de los dos netos; las vecinas salen de `schemas/finance_lines.py`; el comunicado aporta fecha/período, no P&L.

## Oro (no fusionar)

| Riel | Dónde |
|------|--------|
| Contrato IDP | `recipes/financial_statement.json` + `recipes/press_release.json` + `evals/identity_v1.json` + `evals/identity_v2.json` + `evals/press_v1.json` |
| Overlay del chat | `docs/hechos_eeff.json` (`push_hechos.py`) |

1T26: neto `21262335`, controlante `21259769`, bruto `60144176`, operativo `70223471`, impuesto `-14950948`, no controlante `2566`. Página 4. Comunicado 1T26 fecha `2026-05-08`. 2T26 EEFF: primera columna (YTD). Comunicado 2T26 fecha `2026-08-07`.

## Qué falta (producto)

Orden fijo. Un change OpenSpec **nuevo** por slice. No inflar el kernel ni el pin RAGFlow.

1. **Persistir claims** (shipped: [`ledgerlens-claim-store`](../openspec/changes/ledgerlens-claim-store/)).
2. **Comunicado** (shipped: [`ledgerlens-press-release`](../openspec/changes/ledgerlens-press-release/)): fecha + período, no P&L del comunicado.
3. **Después (mismo dominio, mismo corpus):** presentación o transcripción. **No** otros dominios. **No** extraer P&L de memorias.

No ahora: capa 3 RAG, ingresos/EPS, gancho Graph, Compose en ~7 GB. El parse MinerU ya es el camino de identidad vía fixtures.

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
