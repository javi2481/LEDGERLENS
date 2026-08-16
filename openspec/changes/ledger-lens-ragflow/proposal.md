# Proposal: LedgerLens RAGFlow local stack

## Intent

Local portfolio demo: Spanish Q&A over BYMA financial PDFs with citations. Official RAGFlow is UI+RAG; MinerU `pipeline` parses filings (CPU sidecar); Groq `llama-3.3-70b-versatile` is default chat; Voyage is native embed. No evidence → Spanish empty reply, not invention.

## Locked assumptions

User-approved reboot; no question round. Spanish UI; citations; BYMA samples in `docs/archivos_muestra/`. Official `infiniflow/ragflow` **v0.26.4** + Compose overlay (not submodule/from-scratch). Infinity (`DOC_ENGINE=infinity`), not Elasticsearch. Default PDF parser **MinerU** `pipeline` (sidecar `mineru-api:8000`; Naive/DeepDoc fallback). PaddleOCR optional (Compose profile `paddleocr`; `PADDLEOCR_API_URL` commented unless enabled). Default chat: Groq `llama-3.3-70b-versatile` in RAGFlow Model providers. Embed: Voyage native in RAGFlow. Last fallback chat: host Ollama `http://host.docker.internal:11434` (never `127.0.0.1`), `qwen2.5:1.5b`. Forbidden: `app.py`, `ledger_lens/`, Gradio, HF Space, `cloud.ragflow.io`, OpenRouter Nano `:free` as default. Host: x86_64, ≥16 GB RAM, Docker ≥24, Compose ≥v2.26.1, `vm.max_map_count` ≥ 262144. Deferred work: `docs/agenda/`.

## Scope

### In Scope

- Pin RAGFlow `docker/` v0.26.4 in `vendor/ragflow-docker/`; overlay MinerU API + optional `paddleocr` on `ragflow`
- `.env.example`: Infinity, pin, PaddleOCR URL/algorithm, no token; `docker/paddleocr/` CPU `/layout-parsing`
- `scripts/up.sh`: sysctl, compose up, Ollama pull
- `README.md`: start, Empty response + Show Quote, BYMA samples, RAM/x86/Docker
- BYMA sample PDFs in `docs/archivos_muestra/`

### Out of Scope

PP-ChatOCRv4 as product; Excel/CSV; English UI; Gradio/HF/ZeroGPU/custom Python RAG/`app.py`/`ledger_lens/`/`cloud.ragflow.io`; ARM64; Infinity on Linux/arm64.

## Capabilities

> sdd-spec contract. `openspec/specs/` empty. No Gradio spec reuse.

### New Capabilities

- `document-parse`: Ingest BYMA PDFs via RAGFlow **MinerU** `pipeline` by default; Naive/DeepDoc fallback; PaddleOCR optional (PP-StructureV3 CPU; `/layout-parsing`).
- `knowledge-qa`: Spanish answers with citations; Empty response required; no-evidence reply instead of inventing.
- `local-stack`: Official pin; Infinity; Groq chat; host Ollama last fallback via `host.docker.internal`; optional PaddleOCR Compose profile.
- `portfolio-local`: BYMA samples in `docs/archivos_muestra/`; Spanish UI; README for ≥16 GB x86.

### Modified Capabilities

None

## Approach

Approach 1: vendor RAGFlow `docker/` v0.26.4; overlay adds PaddleOCR. `up.sh` runs official compose + overlay. README first-run: Spanish prompt, Empty response, Show Quote.

## Affected Areas

New: `vendor/ragflow-docker/` (pinned official `docker/`); `docker-compose.overlay.yml` (MinerU API + optional PaddleOCR on `ragflow`); `docker/mineru/` (CPU `/file_parse`); `docker/paddleocr/` (CPU `/layout-parsing`); `.env.example`; `scripts/up.sh`; `README.md`; `docs/archivos_muestra/` (BYMA sample PDFs).

## Risks

- RAM overflow (High): Infinity, StructureV3, small models.
- Apply on ~7.4 GB, no Docker (High): smoke only on ≥16 GB x86 + Docker 24+.
- `127.0.0.1` wiring (Med): Compose DNS OCR; `host.docker.internal` Ollama.
- Blank Empty response (Med): spec requires Spanish no-evidence + Show Quote.
- Pin drift (Med): pin v0.26.4. ARM64 (Low): x86_64 only.

## Rollback Plan

`docker compose down -v` drops RAGFlow volumes. Git revert removes overlay, vendor pin, `.env`, PaddleOCR files, fixtures. Host Ollama stays (optional pull-delete).

## Dependencies

Docker ≥24, Compose ≥v2.26.1, x86_64, ≥16 GB RAM, ≥50 GB disk, `vm.max_map_count` ≥ 262144; host Ollama `OLLAMA_HOST=0.0.0.0`; `infiniflow/ragflow:v0.26.4`.

## Success Criteria

- [ ] `scripts/up.sh`: UI port 80, MinerU `/file_parse`, Ollama via `host.docker.internal:11434`
- [ ] BYMA sample PDFs parse; Spanish Q&A cites evidence
- [ ] No-evidence → configured Spanish empty reply
- [ ] No `app.py`, Gradio, HF Space, or `ledger_lens/`; README covers BYMA samples, 16 GB/x86/Docker, Empty response + Show Quote
