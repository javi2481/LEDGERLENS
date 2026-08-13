# Agenda (retomar luego)

Ítems Parallel / stack que **no** entran en el demo actual. Chat default: OpenRouter. Fallback: Ollama. Parser default: **Naive**. Embeddings: OpenRouter `nvidia/nemotron-3-embed-1b:free`.

Consultá un archivo, no todos. Cada uno tiene el porqué, el disparador y el primer paso.

## Quick path

1. Abrí el ítem que vas a retomar.
2. Confirmá el disparador (GPU, 16 GB, parser más rápido, etc.).
3. Seguí el checklist de ese archivo. Los dumps están en `research/`.

## Índice

| Ítem | Cuándo retomarlo |
|------|------------------|
| [TEI embeddings locales](tei-embeddings.md) | Querés embed sin cloud, con RAM de sobra |
| [MinerU / Docling](mineru-docling.md) | Tablas complejas; Naive/DeepDoc no alcanzan |
| [vLLM](vllm.md) | Hay GPU NVIDIA y hace falta más throughput local |
| [Nemotron más grandes](openrouter-larger-models.md) | Nano 30B no alcanza; cuota `:free` lo permite |
| [E2E en host ≥16 GB](e2e-16gb.md) | Esta PC: Docker instalado pero sin grupo/`compose`; RAM 7,4 GB |

## Fuera de esta carpeta (ya hecho)

| Tema | Estado |
|------|--------|
| Parser **Naive** | Default del demo ([nota](naive-parser.md)); DeepDoc fallback |
| Infinity | En el repo |
| PaddleOCR opcional | Profile `paddleocr` |
| OpenRouter chat + embed | README primera vez en la UI |
| Ollama `qwen2.5:1.5b` | Fallback, no default |
| Tests en esta PC | `./scripts/check.sh` |

## Next step

En la **PC ≥16 GB**: [e2e-16gb.md](e2e-16gb.md) y el Quick path del [README raíz](../../README.md). `.env` no está en git: hay que llevar la key de OpenRouter.
