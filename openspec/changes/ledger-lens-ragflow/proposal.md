# Proposal: LedgerLens RAGFlow local stack

## Intent

Local portfolio demo: Spanish Q&A over BYMA financial PDFs with citations. Official RAGFlow is UI+RAG; Docling classic parses filings; OpenRouter is default chat; Voyage is embed; host Ollama is fallback chat. No evidence → Spanish empty reply, not invention.

## Locked assumptions

User-approved reboot; no question round. Spanish UI; citations; BYMA samples in `docs/archivos_muestra/`. Official `infiniflow/ragflow` **v0.26.4** + Compose overlay (not submodule/from-scratch). Infinity (`DOC_ENGINE=infinity`), not Elasticsearch. Default PDF parser **Docling** classic (sidecar; Naive/DeepDoc fallback). PaddleOCR optional (Compose profile `paddleocr`; `PADDLEOCR_API_URL` commented unless enabled). Default chat: OpenRouter (`nvidia/nemotron-3-nano-30b-a3b:free`). Embed: Voyage. Fallback chat: host Ollama `http://host.docker.internal:11434` (never `127.0.0.1`), `qwen2.5:1.5b`. Forbidden: `app.py`, `ledger_lens/`, Gradio, HF Space, `cloud.ragflow.io`. Host: x86_64, ≥16 GB RAM, Docker ≥24, Compose ≥v2.26.1, `vm.max_map_count` ≥ 262144. Deferred work: `docs/agenda/`.

## Scope

### In Scope

- Pin RAGFlow `docker/` v0.26.4 in `vendor/ragflow-docker/`; overlay `paddleocr` on `ragflow`
- `.env.example`: Infinity, pin, PaddleOCR URL/algorithm, no token; `docker/paddleocr/` CPU `/layout-parsing`
- `scripts/up.sh`: sysctl, compose up, Ollama pull
- `README.md`: start, Empty response + Show Quote, synthetic-only, RAM/x86/Docker
- 3–4 Spanish synthetic PDFs in `examples/synthetic/`

### Out of Scope

PP-ChatOCRv4 as product; Excel/CSV; English UI; Gradio/HF/ZeroGPU/custom Python RAG/`app.py`/`ledger_lens/`/`cloud.ragflow.io`; real BYMA; ARM64; Infinity on Linux/arm64.

## Capabilities

> sdd-spec contract. `openspec/specs/` empty. No Gradio spec reuse.

### New Capabilities

- `document-parse`: Ingest BYMA PDFs via RAGFlow **Docling** classic by default; Naive/DeepDoc fallback; PaddleOCR optional (PP-StructureV3 CPU; `/layout-parsing`).
- `knowledge-qa`: Spanish answers with citations; Empty response required; no-evidence reply instead of inventing.
- `local-stack`: Official pin; Infinity; host Ollama chat via `host.docker.internal`; optional PaddleOCR Compose profile.
- `portfolio-local`: Synthetic-only; Spanish UI; README for ≥16 GB x86.

### Modified Capabilities

None

## Approach

Approach 1: vendor RAGFlow `docker/` v0.26.4; overlay adds PaddleOCR. `up.sh` runs official compose + overlay. README first-run: Spanish prompt, Empty response, Show Quote.

## Affected Areas

New: `vendor/ragflow-docker/` (pinned official `docker/`); `docker-compose.overlay.yml` (PaddleOCR on `ragflow`); `docker/paddleocr/` (CPU `/layout-parsing`); `.env.example`; `scripts/up.sh`; `README.md`; `examples/synthetic/` (3–4 fake PDFs).

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

- [ ] `scripts/up.sh`: UI port 80, PaddleOCR `/layout-parsing`, Ollama via `host.docker.internal:11434`
- [ ] 3–4 synthetic PDFs parse; Spanish Q&A cites evidence
- [ ] No-evidence → configured Spanish empty reply
- [ ] No `app.py`, Gradio, HF Space, or `ledger_lens/`; README covers synthetic-only, 16 GB/x86/Docker, Empty response + Show Quote
