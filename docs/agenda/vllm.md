# vLLM (agenda)

Factory local de RAGFlow para más throughput en GPU. [Deploy local models](https://ragflow.io/docs/deploy_local_llm). Dump: `research/stack-ollama-vllm-local.json`.

Ollama queda como fallback CPU. No hay compose vLLM en este repo.

## Quick path

1. Host con GPU NVIDIA + driver.
2. Servir un chat model con vLLM (OpenAI-compatible).
3. Model providers → vLLM. Default chat = ese modelo. Ollama sigue en la UI como fallback.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | GPU disponible y Ollama/OpenRouter no alcanzan latencia |
| Esta PC | Sin GPU útil para vLLM; no implementar |
| Relacionados | Xinference, GPUStack, SGLang — mismo dump, no default |

## Checklist

- [ ] No añadir vLLM al `scripts/up.sh` default
- [ ] URL desde RAGFlow ≠ `127.0.0.1` (Compose DNS o `host.docker.internal`)
- [ ] Empty response y Show Quote no cambian

## Next step

Cuando exista GPU NVIDIA dedicada al demo.
