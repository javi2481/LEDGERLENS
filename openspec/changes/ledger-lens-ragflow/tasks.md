# Tasks: LedgerLens RAGFlow local stack

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350–500 authored; vendor `docker/` pin likely >400 total |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | Single PR (`size:exception`; vendor pin + no PR split) |
| Delivery strategy | auto-chain |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: size-exception
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Vendor pin, overlay OCR, up.sh, fixtures, README | single (`size:exception`) | `test -f vendor/PIN.md && test -f docker-compose.overlay.yml && test -f scripts/up.sh && ls examples/synthetic/*.pdf` | `scripts/up.sh`; `docker compose ps`; README E2E. N/A if no Docker or RAM <16 GB | `vendor/`, `docker-compose.overlay.yml`, `docker/paddleocr/`, `.env.example`, `scripts/up.sh`, `README.md`, `examples/synthetic/`, `.gitignore` |

## Phase 1: Vendor pin and ignores

- [x] 1.1 Copy official `infiniflow/ragflow` `docker/` **v0.26.4** into `vendor/ragflow-docker/` (Apache-2.0); do not edit upstream.
- [x] 1.2 Create `vendor/PIN.md` with tag `v0.26.4`, source URL, and do-not-edit-upstream.
- [x] 1.3 Modify `.gitignore`: keep ignoring root `.env`; ignore `vendor/ragflow-docker/.env`, `ragflow-logs/`, and compose volumes.

## Phase 2: Overlay, OCR image, env

- [x] 2.1 Create `docker/paddleocr/Dockerfile` CPU serve: `paddlex --serve --pipeline PP-StructureV3 --device cpu --host 0.0.0.0 --port 8080` (`POST /layout-parsing`); pin PaddlePaddle 3.x + `paddlex[serving]`.
- [x] 2.2 Create `docker-compose.overlay.yml`: `paddleocr` on network `ragflow`; `build: ./docker/paddleocr`; do **not** publish host `:8080`.
- [x] 2.3 Create `.env.example`: `DOC_ENGINE=infinity`, `COMPOSE_PROFILES=infinity,cpu`, `RAGFLOW_IMAGE=infiniflow/ragflow:v0.26.4`, `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`, PP-StructureV3, no AI Studio token; Ollama `http://host.docker.internal:11434` (never `127.0.0.1`).

## Phase 3: Startup script

- [x] 3.1 Create `scripts/up.sh`: read-only check `vm.max_map_count` ≥ 262144; warn/fail if low and do not claim ready; no `eval` of user strings; no `sysctl -w` unless README documents it.
- [x] 3.2 In `scripts/up.sh`: sync `.env` → `vendor/ragflow-docker/.env`; `docker compose --env-file .env -f vendor/ragflow-docker/docker-compose.yml -f docker-compose.overlay.yml up -d`; document/run `ollama pull qwen2.5:1.5b` and `bge-m3` with `OLLAMA_HOST=0.0.0.0`.

## Phase 4: Synthetic PDFs

- [x] 4.1 Create four Spanish synthetic PDFs in `examples/synthetic/` covering hechos, estados, memoria, and operativo; not real BYMA.

## Phase 5: README, negative scope, verify

- [x] 5.1 Create Spanish `README.md`: x86_64, ≥16 GB, Docker ≥24, Compose ≥v2.26.1, not ARM64; `OLLAMA_HOST=0.0.0.0`; Spanish UI; non-blank Spanish Empty response; Show Quote; synthetic-only; first-run KB/chat.
- [x] 5.2 Add README E2E: ingest four PDFs via Compose-DNS PaddleOCR; in-corpus Spanish + Show Quote; out-of-corpus Spanish Empty (no invention); parser down → visible ingest fail, no fabricated text.
- [x] 5.3 Confirm no `app.py`, `ledger_lens/`, Gradio, HF Space, Compose Ollama, TEI, or Elasticsearch.
- [x] 5.4 Verify: compose healthy (UI `:80`, `paddleocr`, Ollama tags). Manual E2E per README. No pytest (no runner). Skip full smoke if host <16 GB or no Docker.
  - Apply host (~7.4 GB, Docker not installed): runtime smoke skipped; file-level contracts verified (`vendor/PIN.md`, overlay, `up.sh`, four synthetic PDFs, no `app.py`/`ledger_lens`).
