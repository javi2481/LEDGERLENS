# Research dumps (Parallel)

Captured 2026-08-13 with `parallel-cli search` / `extract`. JSON is the source of truth for follow-up. Índice del stack **actual**: **Naive** parser, Infinity, **OpenRouter chat+embed**, Ollama **fallback**, PaddleOCR opcional.

**Decisión (2026-08-13):** chat default = OpenRouter Nemotron Nano `:free`. Ollama `qwen2.5:1.5b` = fallback. Parser **LedgerLens** = Naive. RAGFlow UI sigue ofreciendo DeepDoc como su default de fábrica; el first-run del README elige Naive.

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
| `extract-ragflow-select-pdf-parser.json` | [Select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser) — DeepDoc es el default de **RAGFlow**; LedgerLens usa **Naive** |
| `extract-openrouter-nemotron-embed.json` | [nvidia/nemotron-3-embed-1b:free](https://openrouter.ai/nvidia/nemotron-3-embed-1b:free) |

## Hallazgos (LedgerLens)

- **Compose:** CPU ≥ 4, RAM ≥ 16 GB, disco ≥ 50 GB, Docker ≥ 24, Compose ≥ v2.26.1, imágenes **x86** ([infiniflow/ragflow](https://github.com/infiniflow/ragflow)). UI puerto 80. `DOC_ENGINE=infinity` es switch oficial; ARM64 + Infinity no soportado.
- **Parser default:** **Naive** (texto seleccionable; los fixtures sintéticos lo son). DeepDoc = fallback OCR. PaddleOCR/MinerU/Docling opcionales; RAGFlow es *cliente remoto* de PaddleOCR desde v0.24 ([FAQ](https://ragflow.io/docs/faq), [select PDF parser](https://ragflow.io/docs/dev/select_pdf_parser)).
- **Chat default:** factory **OpenRouter** ([providers](https://ragflow.io/docs/supported_models)), `nvidia/nemotron-3-nano-30b-a3b:free`. **Fallback:** Ollama en `http://host.docker.internal:11434` ([deploy local LLM](https://ragflow.io/docs/deploy_local_llm)), `qwen2.5:1.5b`.
- **Embeddings:** desde v0.22 la imagen slim **no** trae BAAI/Youdao ([upgrade 0.21→0.22](https://ragflow.io/blog/ragflow-seamless-upgrade-from-0.21-to-0.22-and-beyond)). Default: `nvidia/nemotron-3-embed-1b:free` ([OpenRouter](https://openrouter.ai/nvidia/nemotron-3-embed-1b:free)). Factory **NVIDIA** = NIM, distinto de OpenRouter.

## Agenda

Movida a **[docs/agenda/](../docs/agenda/)** (TEI, MinerU/Docling, vLLM, Nemotron grandes, E2E 16 GB). Naive ya está aplicado. Este archivo solo indexa dumps.

## Dumps anteriores (pre-ajuste DeepDoc)

`ragflow-selfhost-paddleocr.json`, `ragflow-faq-paddleocr-extract.json`, `paddleocr-*.json`, `gentle-ai-sdd.json` — útiles para PaddleOCR serving, no para el default actual.

## Relanzar este barrido

```bash
# ejemplos; ajustar objetivos si cambia el pin
parallel-cli search "RAGFlow v0.26.4 Docker Compose Infinity DeepDoc" \
  -q "RAGFlow DeepDoc default PDF parser" --json -o research/stack-ragflow-compose-deepdoc-infinity.json
```
