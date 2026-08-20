# Plan siguiente (producto IDP)

Persistir claims está en curso: [`openspec/changes/ledgerlens-claim-store/`](../openspec/changes/ledgerlens-claim-store/). No inflar `ledgerlens-idp-kernel` ni `ledgerlens-finance-pnl-claims` ni el pin `ledger-lens-ragflow`.

Handoff operativo: [handoff-linux.md](handoff-linux.md).

## 1. Persistencia de claims (activa)

**Problema.** `idp_ask.py` reparseaba el corpus en cada pregunta.

**Decisión.** JSON en `outputs/claims.json` (gitignored). No SQLite ni Postgres. Lookup del CLI lee el store. Reextract con `--refresh` o si cambió un PDF. Evals siguen llamando `extract_claims_from_dir`.

**DoD.**

- Segunda pregunta al mismo corpus: `"store": "hit"` y extract no corre.
- `identity_v1` y `identity_v2` verdes.
- Change `ledgerlens-claim-store`.

**Fuera.** Capa 3 RAG, embeddings, MinerU, overlay Graph.

## 2. Segundo dominio (después)

Una receta `extract: true` que no sea `financial_statement` (p. ej. un campo tipado de `legal_contract` o press_release) + schema + 5–10 gold + pytest. El kernel ya clasifica por receta; hay que demostrar un projector que no sea finanzas.

**Fuera.** Ontología universal. Salud/industria enteros.

## No hacer ahora

- Más filas P&L (ingresos, costos, EPS).
- Router a RAGFlow.
- Gancho Graph nativo.
- `app.py` / `ledger_lens/` / Gradio.

## Cómo arrancar la slice 2 (cuando 1 esté en main)

1. `git pull` y `./scripts/check.sh`.
2. Change OpenSpec **nuevo** (no inflar claim-store).
3. Receta + schema + gold + pytest.
4. Docs del mismo work unit.
