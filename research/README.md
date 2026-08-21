# Research dumps (Parallel)

Captured 2026-08-13 with `parallel-cli search` / `extract`. JSON is the source of truth for follow-up. Índice del stack **actual**: **MinerU** `pipeline` (sidecar CPU), Infinity, chat **Groq** `llama-3.3-70b-versatile` + Ollama fallback, embed **Voyage** nativo, PaddleOCR opcional.

**Decisión (2026-08-16):** parser **LedgerLens** = MinerU `pipeline` vía sidecar `mineru-api:8000`. RAGFlow UI sigue ofreciendo DeepDoc como su default de fábrica; el first-run del README elige MinerU en dataset **`demo_4`**.

**Decisión (2026-08-16, tarde):** chat default = **Groq** `llama-3.3-70b-versatile` (`chat_demo_4`). Gemini `gemini-3.1-flash-lite` se documentó el mismo día pero **no** era el asistente vivo. OpenRouter Nano `:free` queda fuera del default (cuota diaria). Fallback Ollama `qwen2.5:1.5b`. Voyage embed/rerank nativos.

**Decisión (2026-08-16, overlay):** Docling Graph entra al demo: extrae fichas y `push_hechos.py` las inyecta en todos los chats (chunk manual en cada EEFF, sin reparsear PDFs MinerU).

**Decisión (2026-08-20, P&L vecino):** plugin financiero extrae bruto/operativo/EBT/impuesto/no-controlante como claims aparte. Gold en la receta + `evals/identity_v2.json`. `FinancialStatement` no se infla. Overlay `hechos_eeff.json` sigue siendo solo los dos netos.

**Decisión (2026-08-20, higiene):** dos rieles. Producto = kernel IDP (`ledgerlens-idp-kernel`). Demo RAG = pin congelado (`ledger-lens-ragflow`). Oro IDP ≠ overlay `hechos_eeff.json`.

**Decisión (2026-08-20, dominio):** el producto es solo finanzas sobre `docs/archivos_muestra/`. Comunicado y EEFF son tipos de documento del mismo dominio, no un IDP multi-industria. No hay slice de contrato ni otros dominios.

**Decisión (2026-08-20, parse):** un parse MinerU materializado en `fixtures/mineru/`. Clasificar después del texto. `pdftotext` no es parser de identidad. RAGFlow sigue siendo el demo, no la fuente de verdad de identidad.

**Decisión (2026-08-19):** Identity-by-Schema. Catálogo `recipes/` + `schemas/FinancialStatement` (consolidado ≠ controlante). Splink/Zingg/GraphRAG no: fusionan. PixelRAG = RAG visual, no portero. El clasificador/inyección todavía no está.

**Decisión (2026-08-16, mañana, supersedida):** factory Gemini nativa `gemini-3.1-flash-lite` como chat. Ya no es la fuente de verdad.

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
| `extract-reducto-finance-narrative.json` | 10-K parsing; Deep Extract leaderboard |
| `extract-reducto-10k-idp.json` | [Parsing the 10-K](https://reducto.ai/blog/10k-document), GDP.pdf +9 pp, Deep Extract vs humanos |
| `search-mineru-ragflow.json` | RAGFlow cliente MinerU (`MINERU_APISERVER`, `POST /file_parse`); FAQ plugin |
| `extract-mineru-ragflow-plugin.json` | Plugin / env de MinerU en RAGFlow |
| `extract-mineru-github.json` | MinerU API CPU vs imagen GPU `mineru:latest` |
| `search-mineru-hybrid.json` | `hybrid-engine` (GPU); no en v0.26.4 ni en esta APU |
| `extract-mineru-hybrid.json` | Docs hybrid vs pipeline |
| `extract-mineru-hybrid-hw.json` | Hardware hybrid (VRAM) |
| `search-idp-market-2026.json` | IDP agéntico 2026, 10-K |
| `search-reducto-10k-slugs.json` | Slugs reales del blog Reducto |
| `tavily-product.json` | [Tavily](https://www.tavily.com/) + [docs](https://docs.tavily.com/): search/extract/crawl/map/research; 180 ms p50 /search; 1.000 credits gratis |
| `tavily-api-pricing.json` | [Credits](https://docs.tavily.com/documentation/api-credits): planes, costo Search/Extract/Crawl/Research; Hybrid RAG + financial services |
| `ragflow-tavily-agent.json` | RAGFlow ya tiene Tavily: Reasoning + API key desde v0.17; operador Agent desde v0.20 (`tavily_search`) |

## Identity / IDP (2026-08-19)

| Dump | Qué cubre |
|------|-----------|
| `search-idp-classifier-router.json` | Clasificar receta en ingest; no hay router nativo RAGFlow |
| `search-identityrag-reject-option.json` | Abstención / reject option |
| `search-selective-prediction-llm.json` | Selective prediction; entropy sola no basta |
| `search-ragflow-orchestrator.json` | Poll parse DONE; Ingestion Pipeline no rutea schemas |
| `search-oss-idp-orchestrator.json` | No hay orquestador OSS plug-in de RAGFlow 0.26.4 |
| `search-ragflow-agent-switch.json` | Agent Switch = chat, no ingest |
| `search-ragflow-chunk-api.json` | POST/PATCH chunks |
| `extract-ragflow-http-api-chunks.json` | HTTP API add/update chunk |
| `extract-ragflow-ingestion-pipeline.json` | Parser → Transformer → Chunker → Indexer |
| `extract-ragflow-switch.json` | Switch/categorize en agentes |
| `extract-issue-11797.json` | Discussion: PATCH positions vs Show Quote |
| `extract-issue-5648.json` / `extract-issue-8056.json` | Significado de `positions` |
| `extract-issue-13616.json` | MinerU lento post-parse; no prueba polling |
| `search-llamaextract-claims.json` / `extract-llamaextract-*.json` | LlamaExtract = extractor cloud, no router |
| `search-zingg-entity-resolution.json` | Zingg/Splink fusionan registros |
| `search-docling-pathway-extract.json` | Docling extractor / Pathway |
| `search-haystack-llamacloud-classify.json` | Haystack router; LlamaCloud Classify |
| `search-llamacloud-classify-api.json` | type + confidence + unknown |
| `search-groq-langextract-hf.json` | Groq json_schema; LangExtract |
| `extract-langextract-idp-layer.json` | LangExtract grounding |
| `extract-google-docai-classifier.json` | Document AI = patrón, no stack |
| `extract-idp-pipeline-stages.json` / `extract-idp-routing-confidence.json` | IDP classify → extract → abstain |
| `extract-haystack-metadatarouter.json` | MetadataRouter `unmatched` |
| `search-pixelrag.json` | PixelRAG: RAG visual, no identity schema |

## Hallazgos (LedgerLens)

- **Compose:** CPU ≥ 4, RAM ≥ 16 GB, disco ≥ 50 GB, Docker ≥ 24, Compose ≥ v2.26.1, imágenes **x86** ([infiniflow/ragflow](https://github.com/infiniflow/ragflow)). UI puerto 80. `DOC_ENGINE=infinity` es switch oficial; ARM64 + Infinity no soportado.
- **Parser default:** **MinerU** `pipeline` vía sidecar (`MINERU_APISERVER=http://mineru-api:8000`, `MINERU_BACKEND=pipeline`). Naive = fallback texto. DeepDoc = fallback OCR. MinerU hybrid / OpenDataLoader descartados en esta APU. PaddleOCR sigue como profile, no como experimento.
- **Chat default:** **Groq** `llama-3.3-70b-versatile`. Fallback Ollama `qwen2.5:1.5b` (`http://host.docker.internal:11434`). OpenRouter Nano `:free` no es el default.
- **Embeddings (vigente):** Voyage `voyage-finance-2` + rerank `rerank-2.5-lite` nativos en RAGFlow. Desde v0.22 la imagen slim **no** trae BAAI/Youdao ([upgrade 0.21→0.22](https://ragflow.io/blog/ragflow-seamless-upgrade-from-0.21-to-0.22-and-beyond)).
- **Histórico 13-ago (no es el default):** OpenRouter **no** guarda embeddings nativos (`Embedding model from OpenRouter is not supported yet`). Se probó Nano `:free` para chat y Nemotron/Gemini embed; Nano pegó `QUOTA_EXCEEDED`. Factory **NVIDIA** = NIM, distinto de OpenRouter. Chat Gemini 2.5 `404` para keys nuevas. Embed Gemini free: **100 req/min** (`429` en el EEFF largo).
- **Windows:** `*.sh` en LF (`.gitattributes`). `up.sh` lee `/proc/sys/vm/max_map_count` (Git Bash no); Docker Desktop VM ya tiene 262144. Compose se levantó a mano con el mismo `docker compose` que `up.sh`.
- **MinerU (2026-08-16):** sidecar CPU `docker/mineru/Dockerfile` (`mineru[pipeline]==3.4.5`, no `mineru:latest` GPU). Dataset **`demo_4`**, Config MinerU **antes** de subir, `task_page_size=128`. En v0.26.4 el cliente MinerU también manda el PDF entero (`start_page_id=0`); el fix de rangos está en `main`. Timeout 1800 s. Hybrid = GPU + RAGFlow que liste `hybrid-engine`. Informe: `search-mineru-ragflow.json`, `search-mineru-hybrid.json`.

## Agenda

Índice: **[docs/agenda/](../docs/agenda/)** (MinerU pipeline y Groq aplicados; vLLM, LinkedIn, branding diferidos). Descarte: [descartado.md](../docs/agenda/descartado.md). Este archivo solo indexa dumps.

## Dumps anteriores (pre-ajuste DeepDoc)

`ragflow-selfhost-paddleocr.json`, `ragflow-faq-paddleocr-extract.json`, `paddleocr-*.json`, `gentle-ai-sdd.json` — útiles para PaddleOCR serving, no para el default actual.

## Relanzar este barrido

```bash
# ejemplos; ajustar objetivos si cambia el pin
parallel-cli search "RAGFlow v0.26.4 Docker Compose Infinity DeepDoc" \
  -q "RAGFlow DeepDoc default PDF parser" --json -o research/stack-ragflow-compose-deepdoc-infinity.json
```
