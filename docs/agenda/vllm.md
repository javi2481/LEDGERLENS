# vLLM (agenda, GPU NVIDIA)

Tres roles distintos. **Ninguno** en esta PC (Ryzen 8500G, 32 GB, iGPU 740M, sin NVIDIA). No va en `scripts/up.sh`.

Ollama `qwen2.5:1.5b` sigue como fallback CPU de chat. Graph extrae con LLM **remoto** sin vLLM ([docling-graph.md](docling-graph.md)).

[Deploy local models](https://ragflow.io/docs/deploy_local_llm). Dumps: `research/stack-ollama-vllm-local.json`, `research/search-docling-vllm.json`, `research/extract-docling-classic-vlm.json`.

Xinference, GPUStack y SGLang: mismo dump, **descartados** como default ([descartado.md](descartado.md)).

## Los tres roles

| Rol | Comando / binding | Para qué |
|-----|-------------------|----------|
| 1. Chat RAGFlow | Factory vLLM, URL OpenAI-compatible | Throughput local vs OpenRouter |
| 2. Parser VLM | `vllm serve ibm-granite/granite-docling-258M --revision untied` | Pipeline VLM de Docling (no el parser clásico) |
| 3. LLM de Graph | LiteLLM **SDK** `provider_override="vllm"` (dependencia de docling-graph; no un proxy Compose) | Extracción local sin API |

`--revision untied` es obligatorio: los pesos tied rompen vLLM actual ([Granite-Docling 258M](https://huggingface.co/ibm-granite/granite-docling-258M)).

Experimento VLM **sin** vLLM (opcional, no demo): Ollama `ibm/granite-docling:258m`.

## Quick path (cuando haya GPU)

1. Driver NVIDIA. Servir chat **o** Granite-Docling (`untied`) en un puerto (p. ej. 8000 / 1025).
2. Desde RAGFlow: Model providers → vLLM. URL ≠ `127.0.0.1` (Compose DNS o `host.docker.internal`).
3. Desde Docling VLM: `VlmPipeline` → `http://host:8000/v1/chat/completions`.
4. Ollama sigue en la UI como fallback.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | GPU NVIDIA dedicada **y** OpenRouter/Ollama no alcanzan, **o** se quiere VLM local |
| Esta PC | No implementar |
| Parser clásico | [mineru-pipeline.md](mineru-pipeline.md) en CPU; no necesita vLLM |
| CPU vLLM | No. No prometer VLM en APU |

## Checklist

- [ ] No añadir vLLM al `scripts/up.sh` default
- [ ] URL desde contenedores ≠ `127.0.0.1`
- [ ] Empty response y Show Quote no cambian

## Next step

Cuando exista GPU NVIDIA dedicada al demo.
