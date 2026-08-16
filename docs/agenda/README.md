# Agenda (retomar luego)

Ítems que **no** entran en el demo actual. Stack vigente: parser **MinerU** `pipeline` (sidecar CPU), Infinity, chat **Gemini** `gemini-3.1-flash-lite` (factory nativa) + Ollama fallback, embed **Voyage** nativo. Esta PC = Windows Ryzen 8500G 32 GB, **sin NVIDIA**.

Consultá un archivo, no todos. Cada uno tiene disparador, checklist y dumps en `research/`.

Ítems cerrados o rechazados: [descartado.md](descartado.md).

## Quick path

1. Abrí el ítem que vas a retomar.
2. Confirmá el disparador (grafo, GPU, chrome UI, LinkedIn).
3. Seguí el checklist. No implementar sin disparador.

## Activo

| Ítem | Cuándo retomarlo |
|------|------------------|
| [Docling Graph](docling-graph.md) | Comparar períodos / controlante vs consolidado con hechos anclados. LLM remoto. |
| [vLLM](vllm.md) | GPU NVIDIA: chat, Granite-Docling VLM, MinerU hybrid, o LLM local de Graph. |
| [Posicionamiento LinkedIn](posicionamiento-linkedin.md) | Publicar tesis IDP 2026 sin vender Graph/VLM/hybrid no shipped. |
| [Branding cosmético UI](branding-cosmetic.md) | Chrome LedgerLens (logo, nombre, pie Apache-2.0) sin fork. |

## Ya hecho (no es agenda)

| Tema | Estado |
|------|--------|
| Parser **MinerU** `pipeline` | Default del demo ([nota](mineru-pipeline.md)); sidecar `mineru-api:8000` |
| Chat **Gemini** | Default del demo: factory nativa `gemini-3.1-flash-lite`; sin OpenRouter; sin sidecar LiteLLM |
| Embed Voyage | Nativo v0.26.4 en RAGFlow (`VOYAGE_API_KEY` en la UI) |
| Parser Naive | Fallback ([nota](naive-parser.md)); DeepDoc si escaneo |
| E2E Windows 32 GB | Compose + BYMA 1T26 (comunicado, EEFF, presentación) |
| Infinity | En el repo |
| PaddleOCR opcional | Profile `paddleocr` (no es el parser extra) |
| Ollama `qwen2.5:1.5b` | Último fallback de chat, no default |
| Tests | `./scripts/check.sh` |

## Next step

Corpus BYMA en `docs/archivos_muestra/` parseado con MinerU en **`demo_4`** ([runbook](mineru-pipeline.md)). Chat default: Gemini `gemini-3.1-flash-lite`. Después: [plantilla Graph](docling-graph.md) **o** [branding](branding-cosmetic.md) **o** [LinkedIn](posicionamiento-linkedin.md). No retomar TEI ni compose en el Linux de 7 GB. Hybrid MinerU = GPU + RAGFlow que liste el backend.
