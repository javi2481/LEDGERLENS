# vLLM (agenda, GPU NVIDIA)

Roles posibles con NVIDIA. **Ninguno** en esta PC (Ryzen 8500G, 32 GB, iGPU 740M, sin NVIDIA). No va en `scripts/up.sh`.

Ollama `qwen2.5:1.5b` sigue como fallback CPU de chat.

[Deploy local models](https://ragflow.io/docs/deploy_local_llm). Dump: `research/stack-ollama-vllm-local.json`.

Xinference, GPUStack y SGLang: mismo dump, **descartados** como default ([descartado.md](descartado.md)).

## Roles

| Rol | Comando / binding | Para qué |
|-----|-------------------|----------|
| 1. Chat RAGFlow | Factory vLLM, URL OpenAI-compatible | Throughput local vs Groq |
| 2. MinerU hybrid | GPU + backend que RAGFlow liste | Tablas más pesadas que `pipeline` CPU |

## Quick path (cuando haya GPU)

1. Driver NVIDIA. Servir chat en un puerto (p. ej. 8000 / 1025).
2. Desde RAGFlow: Model providers → vLLM. URL ≠ `127.0.0.1` (Compose DNS o `host.docker.internal`).
3. Ollama sigue en la UI como fallback.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | GPU NVIDIA dedicada **y** Groq/Ollama no alcanzan |
| Esta PC | No implementar |
| Parser vigente | [mineru-pipeline.md](mineru-pipeline.md) en CPU; no necesita vLLM |
| CPU vLLM | No |

## Checklist

- [ ] No añadir vLLM al `scripts/up.sh` default
- [ ] URL desde contenedores ≠ `127.0.0.1`
- [ ] Empty response y Show Quote no cambian

## Next step

Cuando exista GPU NVIDIA dedicada al demo.
