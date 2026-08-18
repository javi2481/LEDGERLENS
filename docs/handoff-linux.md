# Handoff — retomar en Linux

Repo: `https://github.com/javi2481/LEDGERLENS` · rama **`main`**. Engram: proyecto **`ledgerlens`**. Gentle AI: `openspec/changes/ledger-lens-ragflow/`.

Abrí este archivo primero. El clone **no** trae volúmenes Docker ni chunks de `demo_4`.

## Máquina

| Host | Qué hacer |
|------|-----------|
| Linux ~7 GB (histórico de verify) | `git pull`. Leé docs. **No** `up.sh` / Compose. |
| Linux ≥16 GB + Docker | `./scripts/check.sh` luego `./scripts/up.sh`. Pegá keys en la UI. Parse MinerU de `docs/archivos_muestra/`. `python scripts/push_hechos.py`. |

No commitear `.env`. Graph **no** va en `up.sh` ni Compose. No reparsear MinerU para “arreglar” Graph. No mencionar un proxy extra de chat al recapear el producto.

## Estado en `main` (ya shipped)

Overlay Graph en el demo: extrae fichas P&L de la **página 4** de los EEFF BYMA y `scripts/push_hechos.py` las pega como chunk manual **en el PDF del EEFF** (Show Quote cita el filing, no un markdown auxiliar).

Oro:

- 1T26 consolidado **21.262.335** vs controlante **21.259.769**
- 2T26 consolidado **81.956.525** vs controlante **81.946.993**

Set de trampas PASS (neto 1T, neto 2T, compare, controlante marzo, controlante junio) con cita al EEFF.

Chat documentado: Groq `llama-3.3-70b-versatile`, umbral **0.3**, Show Quote on, top_n **8**. En Windows, por cuota TPD del 70b, la UI local quedó en `openai/gpt-oss-120b` y top_n **4**. Si hay cuota, volvé al 70b + Top N 8.

## Mañana: no reabrir Graph vs KG

Eso está cerrado. Siguiente paso: **gancho de ingest** (catálogo + umbral + trazabilidad de página). Pregunta lista: [graph-nativo.md](agenda/graph-nativo.md).

Después del gancho, agenda de producto: [branding](agenda/branding-cosmetic.md) o [LinkedIn](agenda/posicionamiento-linkedin.md).

## Arranque rápido

```bash
git clone https://github.com/javi2481/LEDGERLENS.git
cd LEDGERLENS
git pull origin main
```

En Cursor: Engram `mem_context` con proyecto `ledgerlens`. OpenSpec: `openspec/README.md` + `openspec/changes/ledger-lens-ragflow/handoff.md`.
