# Research dumps (Parallel)

Captured 2026-08-13 with `parallel-cli search` / `extract`. JSON is the source of truth for follow-up. Índice del stack **actual**: **MinerU** `pipeline` (sidecar CPU), Infinity, chat **Gemini** `gemini-3.1-flash-lite` (factory nativa) + Ollama fallback, embed **Voyage** nativo, PaddleOCR opcional.

**Decisión (2026-08-16):** parser **LedgerLens** = MinerU `pipeline` vía sidecar `mineru-api:8000`. Docling Serve ya no es el default (cliente v0.26.4 no manda `page_range`, #17450). RAGFlow UI sigue ofreciendo DeepDoc como su default de fábrica; el first-run del README elige MinerU en dataset **`demo_4`**.

**Decisión (2026-08-16):** chat default = factory **Gemini** nativa `gemini-3.1-flash-lite`. Fallback Ollama `qwen2.5:1.5b`. **OpenRouter fuera.** Voyage embed/rerank nativos en RAGFlow. El sidecar LiteLLM se probó y se **revirtió** el mismo día: hop extra innecesario. Los dumps Parallel de ese proxy se borraron. El SDK LiteLLM de Docling Graph no es ese sidecar.

Re-run from repo root:

```bash
cd research
parallel-cli search "<objective>" -q "<keyword>" --json --max-results 10 --excerpt-max-chars-total 27000 -o stack-<topic>.json
parallel-cli extract "<url>" --objective "<focus>" --json > extract-<name>.json
```

## Current stack (2026-08-13)

| Dump | Qué cubre |
|------|-----------|
| `stack-ragflow-compose-deepdoc-infinity.json` | Self-host v0.26.4, 16 GB RAM, x86 images, `vm.max_map_count` ≥ 262144, Infinity vs Elasticsearch |
| `stack-paddleocr-optional-client.json` | PaddleOCR desde v0.24 como cliente remoto; `/layout-parsing`; self-host sin token |
| `stack-ollama-vllm-local.json` | Ollama vs vLLM/Xinference/GPUStack; `host.docker.internal` |
| `stack-embeddings-cloud.json` | v0.22+ sin embeddings en la imagen; OpenAI/Jina/Ollama/TEI |
| `stack-openrouter-nvidia-free.json` | OpenRouter `:free`, Nemotron chat y **embed** NVIDIA |
| `extract-ragflow-deploy-local-llm.json` | [Deploy local models](https://ragflow.io/docs/deploy_local_llm) |
| `extract-ragflow-supported-models.json` | [Model providers](https://ragflow.io/docs/supported_models) |
| `extract-ragflow-faq.json` | [FAQ](https://ragflow.io/docs/faq) (PaddleOCR, Ollama, Infinity) |
| `extract-ragflow-select-pdf-parser.json` | [Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser) — DeepDoc es el default de **RAGFlow**; LedgerLens usa **MinerU** `pipeline` |
| `extract-openrouter-nemotron-embed.json` | [nvidia/nemotron-3-embed-1b:free](https://openrouter.ai/nvidia/nemotron-3-embed-1b:free) |
| `host-32gb-ragflow-ram.json` | RAM/CPU de esta PC Windows (Ryzen 8500G, 32 GB, sin NVIDIA) |
| `host-32gb-ollama-cpu.json` | Ollama en CPU/APU 32 GB |
| `gemini-new-user-models.json` | Keys nuevas: `gemini-2.5-flash` 404; Flash 3.x vigente |
| `gemini-replacement-ids.json` | IDs de reemplazo (`gemini-3.1-flash-lite`, `gemini-3.5-flash`) |
| `ragflow-whitelabel.json` | White-label: no hay no-code; logo/`conf.json`/rebuild. Agenda: [branding-cosmetic.md](../docs/agenda/branding-cosmetic.md) |
| `extract-docling-reducto-hubs.json` | Hubs: [Docling blog](https://docling.ai/blog/), [papers](https://docling.ai/papers/), [docling-graph](https://github.com/docling-project/docling-graph), [Reducto guides](https://reducto.ai/guides/), [blog](https://reducto.ai/blog) |
| `extract-docling-graph-docs.json` | Docs Graph: backends LLM/VLM, provenance, dense extraction, Docling Serve |
| `extract-docling-graph-config.json` | PipelineConfig + PyPI `docling-graph` 1.9.1 (17 jul 2026) |
| `extract-docling-classic-vlm.json` | Parser clásico vs VLM; Granite-Docling + vLLM `untied`; docling-serve |
| `extract-reducto-finance-narrative.json` | 10-K parsing (LlamaIndex vs Docling); Deep Extract leaderboard |
| `extract-reducto-10k-idp.json` | [Parsing the 10-K](https://reducto.ai/blog/10k-document), GDP.pdf +9 pp, Deep Extract vs humanos |
| `search-docling-classic-parser.json` | RAGFlow Docling/`DOCLING_SERVER_URL`; watsonx managed (US$4 / 1.000 pp) |
| `search-docling-graph.json` | Graph + LiteLLM/vLLM/Ollama; doc→grafo 2026 |
| `search-docling-vllm.json` | Granite-Docling / SmolDocling en vLLM; pipeline remoto |
| `search-mineru-ragflow.json` | RAGFlow cliente MinerU (`MINERU_APISERVER`, `POST /file_parse`); FAQ plugin |
| `extract-mineru-ragflow-plugin.json` | Plugin / env de MinerU en RAGFlow |
| `extract-mineru-github.json` | MinerU API CPU vs imagen GPU `mineru:latest` |
| `search-mineru-hybrid.json` | `hybrid-engine` (GPU); no en v0.26.4 ni en esta APU |
| `extract-mineru-hybrid.json` | Docs hybrid vs pipeline |
| `extract-mineru-hybrid-hw.json` | Hardware hybrid (VRAM) |
| `search-idp-market-2026.json` | IDP agéntico 2026, 10-K, GraphRAG |
| `search-reducto-10k-slugs.json` | Slugs reales del blog Reducto |
| `deep-docling-graph-vllm-market.json` | Deep research Parallel (pro-fast): arquitectura ahora/después + LinkedIn |

## Hallazgos (LedgerLens)

- **Compose:** CPU ≥ 4, RAM ≥ 16 GB, disco ≥ 50 GB, Docker ≥ 24, Compose ≥ v2.26.1, imágenes **x86** ([infiniflow/ragflow](https://github.com/infiniflow/ragflow)). UI puerto 80. `DOC_ENGINE=infinity` es switch oficial; ARM64 + Infinity no soportado.
- **Parser default:** **MinerU** `pipeline` vía sidecar (`MINERU_APISERVER=http://mineru-api:8000`, `MINERU_BACKEND=pipeline`). Naive = fallback texto. DeepDoc = fallback OCR. Docling Serve fuera del overlay. MinerU hybrid / OpenDataLoader descartados en esta APU. PaddleOCR sigue como profile, no como experimento.
- **Chat default:** factory **Gemini** nativa `gemini-3.1-flash-lite`. Fallback Ollama `qwen2.5:1.5b` (`http://host.docker.internal:11434`). OpenRouter no entra. LiteLLM sidecar revertido.
- **Embeddings (vigente):** Voyage `voyage-finance-2` + rerank `rerank-2.5-lite` nativos en RAGFlow. Desde v0.22 la imagen slim **no** trae BAAI/Youdao ([upgrade 0.21→0.22](https://ragflow.io/blog/ragflow-seamless-upgrade-from-0.21-to-0.22-and-beyond)).
- **Histórico 13-ago (no es el default):** OpenRouter **no** guarda embeddings nativos (`Embedding model from OpenRouter is not supported yet`). Se probó Nano `:free` para chat y Nemotron/Gemini embed; Nano pegó `QUOTA_EXCEEDED`. Factory **NVIDIA** = NIM, distinto de OpenRouter. Chat Gemini 2.5 `404` para keys nuevas. Embed Gemini free: **100 req/min** (`429` en el EEFF largo).
- **Windows:** `*.sh` en LF (`.gitattributes`). `up.sh` lee `/proc/sys/vm/max_map_count` (Git Bash no); Docker Desktop VM ya tiene 262144. Compose se levantó a mano con el mismo `docker compose` que `up.sh`.
- **MinerU (2026-08-16):** sidecar CPU `docker/mineru/Dockerfile` (`mineru[pipeline]==3.4.5`, no `mineru:latest` GPU). Dataset **`demo_4`**, Config MinerU **antes** de subir, `task_page_size=128`. En v0.26.4 el cliente MinerU también manda el PDF entero (`start_page_id=0`); el fix de rangos está en `main`. Timeout 1800 s. Hybrid = GPU + RAGFlow que liste `hybrid-engine`. Informe: `search-mineru-ragflow.json`, `search-mineru-hybrid.json`.
- **Docling / Graph (2026-08-15, actualizado 16):** parser clásico Docling **ya no** es default. Graph = overlay Pydantic+KG con LLM remoto (agenda). vLLM = tres roles, todos GPU; no en esta APU. Informe: `deep-docling-graph-vllm-market.json`.

## Agenda

Índice: **[docs/agenda/](../docs/agenda/)** (MinerU pipeline y Gemini aplicados; Graph, vLLM, LinkedIn, branding diferidos). Descarte: [descartado.md](../docs/agenda/descartado.md). Este archivo solo indexa dumps.

## Dumps anteriores (pre-ajuste DeepDoc)

`ragflow-selfhost-paddleocr.json`, `ragflow-faq-paddleocr-extract.json`, `paddleocr-*.json`, `gentle-ai-sdd.json` — útiles para PaddleOCR serving, no para el default actual.

## Relanzar este barrido

```bash
# ejemplos; ajustar objetivos si cambia el pin
parallel-cli search "RAGFlow v0.26.4 Docker Compose Infinity DeepDoc" \
  -q "RAGFlow DeepDoc default PDF parser" --json -o research/stack-ragflow-compose-deepdoc-infinity.json
```
