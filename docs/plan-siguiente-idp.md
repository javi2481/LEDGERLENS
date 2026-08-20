# Plan siguiente (producto IDP)

Slice **aún no implementada**. Abrir un change OpenSpec **nuevo**. No inflar `ledgerlens-idp-kernel` ni `ledgerlens-finance-pnl-claims` (ya shipped en `main` / `f63d954`) ni el pin `ledger-lens-ragflow`.

Handoff operativo: [handoff-linux.md](handoff-linux.md). Código de producto ya está en GitHub; local y origin estaban alineados en `f63d954` antes de este archivo.

## 1. Persistencia de claims (hacer primero)

**Problema.** `scripts/idp_ask.py` llama `extract_claims_from_dir()` en cada pregunta: `pdftotext` otra vez sobre los EEFF.

**Alcance.** Guardar los claims extraídos (JSON o SQLite en el repo o en `outputs/`, gitignore si es cache). Lookup lee el store. Reextract solo con flag o si el PDF cambió. No Postgres. No tocar Compose ni `hechos_eeff.json`.

**DoD.**

- Segunda pregunta al mismo corpus no vuelve a parsear si el store está fresco.
- `identity_v1` y `identity_v2` siguen verdes (pueden extraer en el test; el CLI usa el store).
- SDD: `openspec/changes/ledgerlens-claim-store/` (nombre tentativo).

**Fuera.** Capa 3 RAG, embeddings, MinerU.

## 2. Segundo dominio (después)

Una receta `extract: true` que no sea `financial_statement` (p. ej. un campo tipado de `legal_contract` o press_release) + schema + 5–10 gold + pytest. El kernel ya clasifica por receta; hay que demostrar un projector que no sea finanzas.

**Fuera.** Ontología universal. Salud/industria enteros.

## No hacer ahora

- Más filas P&L (ingresos, costos, EPS).
- Router a RAGFlow.
- Gancho Graph nativo.
- `app.py` / `ledger_lens/` / Gradio.

## Cómo arrancar la slice 1

1. `git pull` y `./scripts/check.sh`.
2. Change OpenSpec nuevo (proposal / design / spec / tasks).
3. Store + `idp_ask.py` lee store + test de “no reparsear”.
4. Docs del mismo work unit (este archivo + README si cambia el quick path).
