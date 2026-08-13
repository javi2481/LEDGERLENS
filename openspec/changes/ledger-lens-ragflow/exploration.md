## Exploration: ledger-lens-ragflow

Local Docker Compose stack for LedgerLens: Spanish Q&A over synthetic financial PDFs with citations, using official self-hosted RAGFlow + self-hosted PaddleOCR serving + Ollama. Empty/no-evidence reply instead of inventing. No Gradio, no Hugging Face Space, no custom Python RAG package.

### Current State

The git tree is a bootstrap only (`.gitignore` + SDD init). There is no `docker-compose.yml`, no app code, no test runner. Stale index hits for `ledger-lens-mvp` Gradio specs are phantoms from the wiped history and **must not be reused**. Product, stack, and out-of-scope list are already decided.

Official RAGFlow self-host ([Quickstart](https://ragflow.io/docs/), image [infiniflow/ragflow](https://hub.docker.com/r/infiniflow/ragflow)):

- Clone `infiniflow/ragflow`, check out a stable tag (docs currently show **v0.26.4**), `cd docker`, `docker compose -f docker-compose.yml up -d`.
- Compose includes [`docker/docker-compose.yml`](https://github.com/infiniflow/ragflow/blob/main/docker/docker-compose.yml) + `docker-compose-base.yml` (Elasticsearch **or** Infinity, MySQL, MinIO, Redis). CPU/GPU profiles. UI on host port **80** (`http://localhost`).
- Official compose already sets `extra_hosts: ["host.docker.internal:host-gateway"]` and `env_file: .env`.
- Prerequisites: CPU ≥ 4 cores (x86), RAM ≥ **16 GB**, disk ≥ 50 GB, Docker ≥ 24.0.0, Compose ≥ v2.26.1, `vm.max_map_count` ≥ 262144 ([Quickstart](https://ragflow.io/docs/), [Docker Hub](https://hub.docker.com/r/infiniflow/ragflow)).
- Official images are **x86**; ARM64 needs a custom build ([FAQ](https://ragflow.io/docs/faq), [Build image](https://ragflow.io/docs/build_docker_image)). Infinity on Linux/arm64 is **not** officially supported ([Docker Hub](https://hub.docker.com/r/infiniflow/ragflow)).
- Switch engine: `DOC_ENGINE=infinity` in `docker/.env` after `docker compose down -v` ([FAQ](https://ragflow.io/docs/faq)). Infinity uses less RAM than Elasticsearch.
- PaddleOCR is a **remote client from v0.24**: `PADDLEOCR_API_URL` + `PADDLEOCR_ALGORITHM` (default `PaddleOCR-VL`). Self-host needs **no** AI Studio token. FAQ example URL `http://localhost:8080/layout-parsing` is correct **on the host**, not from inside the RAGFlow container ([FAQ](https://ragflow.io/docs/faq)).
- Ollama from a RAGFlow container must be `http://host.docker.internal:11434`, **not** `127.0.0.1` ([Deploy local LLM](https://ragflow.io/docs/deploy_local_llm)). Set `OLLAMA_HOST=0.0.0.0` on the host. RAGFlow also needs a **local embedding** model (docs suggest `bge-m3` via Ollama).
- Grounding: Chat assistant **Empty response** confines answers to the dataset; leaving it blank lets the LLM improvise ([Quickstart](https://ragflow.io/docs/)). Enable **Show Quote** for citations. UI includes Spanish as a community language ([release notes](https://ragflow.io/docs/release_notes)).

Official PaddleOCR serving ([serving docs](https://www.paddleocr.ai/latest/en/version3.x/deployment/serving.html), [main serving](https://www.paddleocr.ai/main/en/version3.x/inference_deployment/serving/serving.html)): `paddlex --serve --pipeline {name}` on `0.0.0.0:8080`; `--device` defaults to GPU if present else CPU. Layout-parsing path expected by RAGFlow: `/layout-parsing`. CPU-first: PP-StructureV3 is lighter than PaddleOCR-VL (0.9B VLM).

This investigation host: **x86_64**, `vm.max_map_count=1048576` (OK), **~7.4 GB RAM** (below the 16 GB minimum), **Docker not installed**. Target demo machine is assumed 16 GB as declared.

### Affected Areas

New files only (empty repo). Do not introduce `app.py`, `ledger_lens/`, Gradio, or HF Space.

- `docker-compose.yml` or overlay — include official RAGFlow compose + PaddleOCR service on the `ragflow` network
- `vendor/ragflow-docker/` or submodule `third_party/ragflow` — pinned official `docker/` assets (`docker-compose-base.yml`, nginx, `service_conf.yaml.template`, `entrypoint.sh`, `.env`)
- `.env.example` — `DOC_ENGINE=infinity`, pinned `RAGFLOW_IMAGE`/`RAGFLOW_VERSION`, `PADDLEOCR_API_URL`, `PADDLEOCR_ALGORITHM`, no access token
- `docker/paddleocr/` — thin CPU Dockerfile wrapping official PaddleOCR serving (`/layout-parsing`)
- `scripts/up.sh` — sysctl check, compose up, Ollama pull (`qwen2.5:1.5b` + embedding)
- `README.md` — local startup, Spanish UI, Empty response, synthetic-only disclaimer
- `examples/synthetic/` — Spanish fake financial PDFs (not real BYMA)
- `openspec/changes/ledger-lens-ragflow/` — this change; ignore any Gradio delta specs

### Approaches

1. **Official pin + Compose overlay** — Pin RAGFlow `docker/` at a stable tag (e.g. v0.26.4, ≥ v0.24 for PaddleOCR client). Overlay adds `paddleocr` (and optionally `ollama`) on network `ragflow`. `scripts/up.sh` runs official compose + overlay with `.env`.
   - Pros: Stays on upstream compose (MySQL/MinIO/Redis/Infinity, extra_hosts, CPU profile); smallest custom surface; matches decided stack.
   - Cons: Must vendor or submodule upstream `docker/` files; overlay must track tag upgrades (e.g. MinIO image change in v0.25).
   - Effort: Medium

2. **Git submodule of full infiniflow/ragflow** — Submodule the whole upstream repo; overlay beside it.
   - Pros: Easy tag bumps; Apache-2.0 provenance clear.
   - Cons: Huge tree for a portfolio demo; accidental upstream-app edits; worse onboarding.
   - Effort: Medium

3. **From-scratch Compose** — Rewrite all RAGFlow deps plus PaddleOCR/Ollama in this repo.
   - Pros: One small compose file.
   - Cons: High drift from official healthchecks/nginx/env; fights the "use official RAGFlow" decision; High maintenance.
   - Effort: High

Nested choices (apply inside approach 1):

| Choice | Prefer | Why |
|--------|--------|-----|
| Document engine | **Infinity** | Lower RAM than Elasticsearch; official switch via `DOC_ENGINE` ([FAQ](https://ragflow.io/docs/faq)). Avoid on Linux/arm64. |
| PaddleOCR algorithm | **PP-StructureV3 on CPU default**; `PaddleOCR-VL` optional | 16 GB must also hold RAGFlow + Ollama chat + embedding. VL is heavier. Same `/layout-parsing` client. |
| PaddleOCR URL from RAGFlow | **`http://paddleocr:8080/layout-parsing`** (Compose DNS) | FAQ `localhost:8080` is wrong inside the RAGFlow container. Host-only PaddleOCR would use `http://host.docker.internal:8080/layout-parsing`. |
| Ollama | **Host Ollama + `http://host.docker.internal:11434`** as primary; optional Compose `ollama` service using `http://ollama:11434` | Matches official docs and the decided URL. Compose service is a documented alternative for one-command `up.sh`. |
| Embedding | **Ollama `bge-m3` (or similarly small multilingual)** | RAGFlow Q&A needs embeddings, not only the chat model ([Deploy local LLM](https://ragflow.io/docs/deploy_local_llm)). |

### Recommendation

**Approach 1 (official pin + overlay)** with Infinity, CPU PaddleOCR (PP-StructureV3 default, VL overridable), host Ollama at `http://host.docker.internal:11434`, PaddleOCR on the Compose network.

Deliverable shape:

- Pin RAGFlow ≥ v0.24 (prefer current stable **v0.26.4**).
- `.env.example`: `DOC_ENGINE=infinity`, `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`, `PADDLEOCR_ALGORITHM=PP-StructureV3` (or `PaddleOCR-VL`), omit `PADDLEOCR_ACCESS_TOKEN`.
- Chat assistant: Spanish system prompt, **Empty response** set to a Spanish no-evidence line, **Show Quote** on, dataset = synthetic PDFs only.
- README: `vm.max_map_count`, 16 GB RAM, x86 images, Ollama `OLLAMA_HOST=0.0.0.0`, first-run UI steps, synthetic-only / not BYMA.
- Out of scope unchanged: `cloud.ragflow.io`, PP-ChatOCRv4 as the product, Excel/CSV, English UI as the demo default, HF Space, Gradio.

Do not reopen Gradio/HF. Do not reuse `ledger-lens-mvp` specs.

### Risks

- **RAM**: Official RAGFlow alone wants ≥ 16 GB. Adding PaddleOCR CPU + Ollama (`qwen2.5:1.5b` + `bge-m3`) can exceed 16 GB, especially with Elasticsearch or PaddleOCR-VL. Mitigate: Infinity, small models, StructureV3 CPU, no concurrent heavy parses. **This host has ~7.4 GB and no Docker** — apply/verify here will fail unless run on a ≥16 GB x86 machine with Docker 24+.
- **ARM**: No official RAGFlow images; Infinity unsupported on Linux/arm64. Demo target is **x86_64** (this host is x86_64).
- **Wiring**: `127.0.0.1` inside RAGFlow does not reach host Ollama or host PaddleOCR. Use `host.docker.internal` (official compose already maps `host-gateway`) or Compose service DNS.
- **Empty-response footgun**: Blank **Empty response** → hallucination, violating the product rule. Specs must require that field.
- **Pin drift**: Nightly/`latest` can migrate schemas (e.g. MinIO image in v0.25). Pin a stable tag.
- **CPU parse latency**: PaddleOCR-VL on CPU may stall ingestion; FAQ notes parse killed by insufficient RAM ([FAQ](https://ragflow.io/docs/faq)).
- **No test runner**: Compose smoke (`curl` UI, PaddleOCR health, Ollama tags) only until a runner exists (`strict_tdd: false`).

### Ready for Proposal

Yes. Orchestrator should run **sdd-propose** for `ledger-lens-ragflow` with capabilities `document-parse`, `knowledge-qa`, `local-stack`, `portfolio-local` (new domains — do not copy Gradio specs). Call out the 16 GB / Docker / x86 constraints and Empty-response configuration as non-optional.

### Sources

- [RAGFlow Quickstart](https://ragflow.io/docs/)
- [RAGFlow FAQ](https://ragflow.io/docs/faq)
- [RAGFlow Deploy Local Models](https://ragflow.io/docs/deploy_local_llm)
- [RAGFlow Build Docker image](https://ragflow.io/docs/build_docker_image)
- [RAGFlow release notes](https://ragflow.io/docs/release_notes)
- [infiniflow/ragflow docker-compose.yml](https://github.com/infiniflow/ragflow/blob/main/docker/docker-compose.yml)
- [infiniflow/ragflow Docker Hub](https://hub.docker.com/r/infiniflow/ragflow)
- [PaddleOCR serving (latest)](https://www.paddleocr.ai/latest/en/version3.x/deployment/serving.html)
- [PaddleOCR self-hosted serving (main)](https://www.paddleocr.ai/main/en/version3.x/inference_deployment/serving/serving.html)
