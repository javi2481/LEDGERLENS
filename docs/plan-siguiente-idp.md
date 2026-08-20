# Plan siguiente (producto IDP)

Comunicado es el change activo: [`openspec/changes/ledgerlens-press-release/`](../openspec/changes/ledgerlens-press-release/). Cache shipped: [`ledgerlens-claim-store`](../openspec/changes/ledgerlens-claim-store/). No inflar kernel, P&L, claim-store ni el pin `ledger-lens-ragflow`.

Handoff operativo: [handoff-linux.md](handoff-linux.md).

## 1. Persistencia de claims (shipped)

JSON en `outputs/claims.json`. CLI reusa el cache; `--refresh` reextrae. Evals extraen siempre.

## 2. Comunicado (activa)

Fecha de anuncio + período cubierto. No la tabla P&L del PDF. Gold: 1T26 `2026-05-08` / `2026-03-31`; 2T26 `2026-08-07` / `2026-06-30`. Neto o impuesto “del comunicado” sigue abstain.

## 3. Después: legal_contract

Hace falta un PDF de fixture (hoy no hay contratos en `docs/archivos_muestra/`). Change OpenSpec **nuevo**.

**Fuera.** Ontología universal. Salud/industria enteros. Más filas P&L. RAG. Graph. Compose. `app.py`.
