# Delta for local-stack

## ADDED Requirements

### Requirement: Official pin Infinity Docling default

Runtime MUST be Docker Compose with official `infiniflow/ragflow` **v0.26.4**. Engine MUST be Infinity (`DOC_ENGINE=infinity`). Default PDF parser MUST be Docling classic via sidecar (`DOCLING_SERVER_URL=http://docling-serve:5001`, `USE_DOCLING=false`). The PaddleOCR overlay MUST be optional (Compose profile `paddleocr`). MUST NOT include `app.py`, `ledger_lens/`, Gradio, HF Space, or `cloud.ragflow.io`.

#### Scenario: Pinned stack starts without forbidden apps

- GIVEN Docker ≥24, Compose ≥v2.26.1, x86_64, ≥16 GB RAM
- WHEN `scripts/up.sh` runs with default `.env`
- THEN UI SHALL be on port 80 with tag v0.26.4; `paddleocr` SHALL NOT be required; `app.py`/Gradio/`ledger_lens/` MUST NOT exist

### Requirement: OpenRouter chat default, Ollama fallback, cloud embeddings

RAGFlow MUST use **OpenRouter** as the default chat (`nvidia/nemotron-3-nano-30b-a3b:free`) and embedding (`nvidia/nemotron-3-embed-1b:free`) via Model providers (the v0.22+ image has no built-in BAAI/Youdao). Host Ollama at `http://host.docker.internal:11434` (not `127.0.0.1`) MUST remain the **fallback** chat (`qwen2.5:1.5b`). `.env.example` MUST set Infinity and the image pin; PaddleOCR URL/algorithm MUST be commented unless the optional profile is used. `scripts/up.sh` MUST check `vm.max_map_count` ≥ 262144, start compose, and MAY pull the Ollama fallback model. RAGFlow MUST NOT auto-read `OPENROUTER_API_KEY`; the operator MUST paste it in the UI.

#### Scenario: OpenRouter is default chat

- GIVEN OpenRouter is configured in Model providers with the Nano `:free` chat model
- WHEN the operator follows README first-run
- THEN System Model Settings chat default MUST be OpenRouter, not Ollama

#### Scenario: Ollama fallback via host-gateway

- GIVEN host Ollama on `0.0.0.0:11434` and `.env` from `.env.example`
- WHEN OpenRouter is unavailable and RAGFlow uses the fallback chat model
- THEN requests MUST use `http://host.docker.internal:11434`

#### Scenario: Low vm.max_map_count fails fast

- GIVEN `vm.max_map_count` below 262144
- WHEN `scripts/up.sh` runs
- THEN the script MUST warn or fail and MUST NOT claim the demo is ready
