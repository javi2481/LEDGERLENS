# Handoff — retomar en otra PC

Repo: `https://github.com/javi2481/LEDGERLENS` · rama **`main`**. Engram: proyecto **`ledgerlens`**.

Abrí este archivo primero. Un parse MinerU, dos capas (claims tipados y chat RAGFlow). El clone trae `fixtures/mineru/*.md`; **no** trae volúmenes Docker ni chunks de `demo_4`.

## Quick path

```bash
git pull origin main
uv venv && uv pip install -r requirements-dev.txt
./scripts/check.sh
python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"
# → 21262335
python scripts/idp_ask.py "¿Cuál es la fecha del comunicado de prensa 1T26?"
# → 2026-05-08
python scripts/idp_ask.py "¿Cuál es el EBITDA de la presentación 1T26?"
# → 72128
```

Siguiente: [plan-siguiente-idp.md](plan-siguiente-idp.md). Corpus = `docs/archivos_muestra/`. No otros dominios.

OpenSpec activo: [`ledgerlens-results-presentation`](../openspec/changes/ledgerlens-results-presentation/). Shipped: kernel, P&L, claim-store, press-release, mineru-parse, product-shape, claims-to-rag. Pin UI/stack: [`ledger-lens-ragflow`](../openspec/changes/ledger-lens-ragflow/) — no inflar.

## Máquina

| Host | Qué hacer |
|------|-----------|
| Linux ~7 GB | IDP + docs. **No** Compose. |
| Linux ≥16 GB + Docker | IDP + UI: `./scripts/up.sh` + MinerU + `python scripts/push_claims.py` (chat nuevo). |

No commitear `.env`. El inject **no** va en `up.sh`. Identidad = `fixtures/mineru/` + pytest. En la PC con stack: `python scripts/export_mineru.py` pisa los artefactos con chunks de `demo_4`. Tras merge: `python scripts/push_claims.py` y chat nuevo.

## Hecho

Kernel extract + lookup, P&L vecino, claim-store, comunicado (fecha/período), presentación (EBITDA + margen LTM), parse MinerU, inject de claims al chat.

Dominio: finanzas BYMA. `FinancialStatement` es el portero de los dos netos; las vecinas salen de `schemas/finance_lines.py`; el comunicado aporta fecha/período.

## Oro

| Rol | Dónde |
|-----|--------|
| Contrato IDP | recipes + identity_v1/v2 + press_v1 + presentation_v1 |
| Inject chat | claims del kernel vía `scripts/push_claims.py` (no un JSON gemelo) |

1T26: neto `21262335`, controlante `21259769`, bruto `60144176`, operativo `70223471`, impuesto `-14950948`, no controlante `2566`. Página 4. Comunicado 1T26 fecha `2026-05-08`. Presentación 1T26 EBITDA `72128` / margen LTM `76`. 2T26 EEFF: primera columna (YTD). Comunicado 2T26 fecha `2026-08-07`. Presentación 2T26 EBITDA `71697` / margen LTM `75`.

## Qué falta

Un change OpenSpec **nuevo** por slice. No inflar kernel ni el pin RAGFlow.

1. **No** extraer P&L de memorias. Transcripción después.

## Arranque

```bash
git clone https://github.com/javi2481/LEDGERLENS.git
cd LEDGERLENS
git pull origin main
```

Engram `mem_context` con proyecto `ledgerlens`. OpenSpec: `openspec/README.md`.
