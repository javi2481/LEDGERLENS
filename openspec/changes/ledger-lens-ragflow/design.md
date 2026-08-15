# Design: LedgerLens RAGFlow local stack

Vendor official RAGFlow `docker/` **v0.26.4**. Default parser **Docling** classic (sidecar CPU). Naive/DeepDoc fallback. Optional PaddleOCR overlay (Compose profile `paddleocr`). Default chat: **OpenRouter** (Nemotron Nano `:free`). Embed: **Voyage**. Host Ollama is **fallback** chat only. Infinity for lower RAM. No `app.py`, `ledger_lens/`, Gradio, HF Space.

## Technical Approach

`scripts/up.sh` starts official compose (overlay file loaded; `paddleocr` service idle unless profile enabled). RAGFlow UI **:80** is the product. First-run KB/chat (Spanish, Empty response, Show Quote, OpenRouter) lives in README, not code. Deferred items live in `docs/agenda/`. Host-level checks: `scripts/check.sh`.

## Architecture Decisions

| Decision | Choice | Rejected | Why |
|----------|--------|----------|-----|
| Stack shape | Vendor `docker/` v0.26.4 + optional overlay | Submodule; from-scratch compose | Keeps MySQL/MinIO/Redis/Infinity, `extra_hosts`, CPU profile |
| Doc engine | `DOC_ENGINE=infinity` (`COMPOSE_PROFILES=infinity,cpu`) | Elasticsearch / OpenSearch | Lower RAM; official switch. Not Linux/arm64 |
| PDF parser | **Docling** classic sidecar | Naive as default; PaddleOCR as default; Granite-Docling VLM | EEFF BYMA need layout + tables ([Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser)). Naive/DeepDoc remain fallback. VLM needs NVIDIA |
| Optional OCR | Profile `paddleocr` + commented env | Always-on PaddleOCR | Keep PaddleOCR as an alternate parser without paying RAM at boot |
| OCR URL (when enabled) | `http://paddleocr:8080/layout-parsing` | FAQ `localhost:8080` | `localhost` inside RAGFlow is the container |
| LLM | OpenRouter chat default; Ollama fallback `http://host.docker.internal:11434` | Compose `ollama`; vLLM now | Cloud `:free` for demo quality; Ollama if OpenRouter is down |
| Embed | OpenRouter `nvidia/nemotron-3-embed-1b:free` | Built-in BAAI/Youdao; TEI; Ollama `bge-m3` | v0.22+ image has no built-in embeddings; TEI is agenda |
| Chat model | `nvidia/nemotron-3-nano-30b-a3b:free` | 7B+ in-compose; Ultra 550B | Nano is the `:free` default; larger Nemotron in `docs/agenda/` |

## Data Flow

```mermaid
sequenceDiagram
  actor User
  participant UI as RAGFlow :80
  participant RF as ragflow-cpu
  participant DS as docling-serve :5001
  participant Inf as infinity
  participant Min as minio
  User->>UI: upload BYMA PDF
  UI->>RF: parse (Docling default)
  RF->>DS: convert /v1/convert/source
  DS-->>RF: markdown + layout
  RF->>Min: store
  RF->>Inf: chunks+embed (Voyage)
  Inf-->>RF: indexed
  RF-->>UI: done
```

```mermaid
sequenceDiagram
  actor User
  participant UI as RAGFlow :80
  participant RF as ragflow-cpu
  participant Inf as infinity
  participant OR as OpenRouter
  participant Ol as host Ollama :11434
  User->>UI: Spanish question
  UI->>RF: chat
  RF->>Inf: retrieve
  alt hits
    Inf-->>RF: chunks
    alt OpenRouter default
      RF->>OR: nemotron-3-nano-30b-a3b:free
      OR-->>RF: answer
    else Ollama fallback
      RF->>Ol: qwen2.5:1.5b
      Ol-->>RF: answer
    end
    RF-->>UI: Spanish + quotes
  else no hits
    RF-->>UI: Spanish Empty response
  end
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `vendor/ragflow-docker/` | Create | Pin `infiniflow/ragflow` `docker/` v0.26.4 (Apache-2.0) |
| `vendor/PIN.md` | Create | Tag, source URL, do-not-edit-upstream |
| `docker-compose.overlay.yml` | Create | Optional `paddleocr` (profile); do not publish 8080 |
| `docker/paddleocr/Dockerfile` | Create | `paddlex --serve --pipeline PP-StructureV3 --device cpu --host 0.0.0.0 --port 8080` |
| `.env.example` | Create | Infinity, `RAGFLOW_IMAGE=infiniflow/ragflow:v0.26.4`; PaddleOCR vars commented |
| `scripts/up.sh` | Create | Read-only `vm.max_map_count` ≥ 262144; sync `.env` → vendor; compose both files; optional `ollama pull qwen2.5:1.5b` fallback |
| `scripts/check.sh` | Create | File contracts, PDF fixtures, host probe; optional OpenRouter smoke |
| `docs/agenda/` | Create | Deferred: TEI, MinerU/Docling, vLLM, larger Nemotron, E2E 16 GB |
| `README.md` | Create | x86_64, ≥16 GB, Docker ≥24, Compose ≥v2.26.1; `OLLAMA_HOST=0.0.0.0`; Empty response + Show Quote; synthetic-only |
| `examples/synthetic/*.pdf` | Create | 3–4 Spanish fake financial PDFs |
| `.gitignore` | Modify | Keep `.env`; ignore vendor `.env` and `ragflow-logs/` |

Do **not** create: `app.py`, `ledger_lens/`, Gradio, HF Space, Compose Ollama, TEI as default, Elasticsearch.

## Interfaces / Contracts

```bash
docker compose --env-file .env \
  -f vendor/ragflow-docker/docker-compose.yml \
  -f docker-compose.overlay.yml up -d
```

Vendor relative paths stay valid. Overlay `build: ./docker/paddleocr` is repo-root-relative. Same project merges `ragflow`. Sync `.env` into vendor because official `env_file: .env`.

| Contract | Value |
|----------|--------|
| UI | `http://localhost` (`SVR_WEB_HTTP_PORT=80`) |
| OCR | Docling classic default (sidecar :5001); Naive/DeepDoc fallback; optional DNS `paddleocr` + `POST /layout-parsing` |
| LLM | OpenRouter default; Ollama fallback `http://host.docker.internal:11434` (never container `127.0.0.1`) |
| Empty response | Non-blank Spanish no-evidence line (copy owned by spec) |

## Testing Strategy

No runner (`strict_tdd: false`). Smoke only on ≥16 GB x86 + Docker 24+ Compose v2 (this host ~7.4 GB; Docker CLI installed, no `docker` group, no Compose plugin).

| Layer | What | Approach |
|-------|------|----------|
| Unit | N/A | No app package |
| Integration | UI :80; OpenRouter in UI; Ollama fallback tag | `scripts/check.sh`; `curl` / `compose ps` on ≥16 GB |
| E2E | Parse PDFs; cite; no-evidence | Manual per README |

## Threat Matrix

`up.sh` is an explicit shell entrypoint (compose + `ollama pull` + sysctl **read**). Not VCS/PR automation.

| Boundary | Applicability | Design response | Planned RED tests |
|----------|---------------|-----------------|-------------------|
| Documentation-like paths | N/A: does not execute README/`requirements.txt`/MDX | — | none |
| Git repository selection | N/A: no git | — | none |
| Commit state | N/A: no commits | — | none |
| Push state | N/A: no push | — | none |
| PR commands | N/A: no `gh` | — | none |

`up.sh` must not `eval` user strings, must not `sysctl -w` unless documented, must not publish `:8080`.

## Migration / Rollout

No migration. Rollback: `docker compose down -v`; git revert overlay/vendor/env/scripts/fixtures. Host Ollama remains.

## Open Questions

- [ ] Exact Spanish Empty-response string — spec owns; design requires non-blank.
- [ ] PaddleOCR image digest — pin at apply (CPU PaddlePaddle 3.x + `paddlex[serving]`).
