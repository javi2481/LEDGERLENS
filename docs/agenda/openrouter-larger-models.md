# Nemotron más grandes en OpenRouter (agenda)

Default de chat: `nvidia/nemotron-3-nano-30b-a3b:free`. Alternativas `:free` vistas en Parallel: Lightning y Ultra 550B. Cuota típica ~200 req/día.

Ultra es enorme y poco fiable para un demo. No cambiar el default sin E2E.

## Quick path

1. En Model providers → OpenRouter, añadir el modelo extra.
2. Probar una pregunta in-corpus y una out-of-corpus.
3. Si es estable, documentar en README como opción, no como único default.

## Details

| Modelo | Uso |
|--------|-----|
| `nvidia/nemotron-3-nano-30b-a3b:free` | Default |
| `nvidia/nemotron-3.5-lightning:free` | Probar si Nano se queda corto |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Último recurso; rate-limit / timeouts |
| Factory **NVIDIA** (NIM) | Distinto de OpenRouter; no mezclar |

Dump: `research/stack-openrouter-nvidia-free.json`.

## Checklist

- [ ] Empty response sigue en español, sin invención
- [ ] Show Quote sigue activo
- [ ] No commitear la API key

## Next step

Solo después del E2E con Nano en un host ≥16 GB.
