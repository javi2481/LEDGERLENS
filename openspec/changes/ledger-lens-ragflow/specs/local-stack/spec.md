# Delta for local-stack

## ADDED Requirements

### Requirement: Official pin Infinity MinerU default

Runtime MUST be Docker Compose with official `infiniflow/ragflow` **v0.26.4**. Engine MUST be Infinity (`DOC_ENGINE=infinity`). Default PDF parser MUST be MinerU `pipeline` via sidecar (`MINERU_APISERVER=http://mineru-api:8000`, `MINERU_BACKEND=pipeline`, `USE_DOCLING=false`). `.env.example` MUST NOT set `DOCLING_SERVER_URL`. The PaddleOCR overlay MUST be optional (Compose profile `paddleocr`). MUST NOT include `app.py`, `ledger_lens/`, Gradio, HF Space, or `cloud.ragflow.io`.

#### Scenario: Pinned stack starts without forbidden apps

- GIVEN Docker ≥24, Compose ≥v2.26.1, x86_64, ≥16 GB RAM
- WHEN `scripts/up.sh` runs with default `.env`
- THEN UI SHALL be on port 80 with tag v0.26.4; `mineru-api` SHALL be required; `paddleocr` SHALL NOT be required; `app.py`/Gradio/`ledger_lens/` MUST NOT exist

### Requirement: Gemini chat, Ollama last fallback, Voyage embeddings

RAGFlow MUST use the native **Gemini** factory as the default chat: model `gemini-3.1-flash-lite`. Last fallback MUST be host Ollama `qwen2.5:1.5b` at `http://host.docker.internal:11434` (not `127.0.0.1`). MUST NOT include a LiteLLM Compose sidecar. MUST NOT route OpenRouter. Embeddings and rerank MUST remain Voyage via RAGFlow Model providers. `.env.example` MUST set Infinity and the image pin; MUST keep `GEMINI_API_KEY` commented; MUST NOT set `OPENROUTER_API_KEY` or `LITELLM_MASTER_KEY`. `scripts/up.sh` MUST check `vm.max_map_count` ≥ 262144, start compose (MinerU sidecar, no `litellm`), and MAY pull the Ollama fallback model. RAGFlow MUST NOT auto-read provider keys; the operator MUST paste Gemini (and Voyage) in the UI.

#### Scenario: Gemini is default chat

- GIVEN Gemini is configured in Model providers with model `gemini-3.1-flash-lite`
- WHEN the operator follows README first-run
- THEN System Model Settings chat default MUST be Gemini, not OpenRouter, Ollama, or OpenAI-API-Compatible

#### Scenario: Ollama last fallback via host-gateway

- GIVEN host Ollama on `0.0.0.0:11434` and `.env` from `.env.example`
- WHEN Gemini is unavailable and the operator switches chat to Ollama
- THEN requests MUST use `http://host.docker.internal:11434`

#### Scenario: Low vm.max_map_count fails fast

- GIVEN `vm.max_map_count` below 262144
- WHEN `scripts/up.sh` runs
- THEN the script MUST warn or fail and MUST NOT claim the demo is ready
