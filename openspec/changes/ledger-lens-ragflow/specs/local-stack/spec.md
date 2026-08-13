# Delta for local-stack

## ADDED Requirements

### Requirement: Official pin overlay Infinity

Runtime MUST be Docker Compose with official `infiniflow/ragflow` **v0.26.4** plus a PaddleOCR overlay on `ragflow`. Engine MUST be Infinity (`DOC_ENGINE=infinity`). MUST NOT include `app.py`, `ledger_lens/`, Gradio, HF Space, or `cloud.ragflow.io`.

#### Scenario: Pinned stack starts without forbidden apps

- GIVEN Docker ≥24, Compose ≥v2.26.1, x86_64, ≥16 GB RAM
- WHEN `scripts/up.sh` runs
- THEN UI SHALL be on port 80 with tag v0.26.4; `app.py`/Gradio/`ledger_lens/` MUST NOT exist

### Requirement: Host Ollama env and up script

RAGFlow MUST use host Ollama at `http://host.docker.internal:11434` (not `127.0.0.1`) for chat/embeddings (`qwen2.5:1.5b`, `bge-m3`). `.env.example` MUST set Infinity, pin, PaddleOCR URL/algorithm, no token. `scripts/up.sh` MUST check `vm.max_map_count` ≥ 262144, start compose+overlay, and pull Ollama models.

#### Scenario: Ollama via host-gateway and env start

- GIVEN host Ollama on `0.0.0.0:11434` and `.env` from `.env.example`
- WHEN `scripts/up.sh` runs and RAGFlow uses LLM/embedding
- THEN requests MUST use `http://host.docker.internal:11434`; overlay SHALL be up

#### Scenario: Low vm.max_map_count fails fast

- GIVEN `vm.max_map_count` below 262144
- WHEN `scripts/up.sh` runs
- THEN the script MUST warn or fail and MUST NOT claim the demo is ready
