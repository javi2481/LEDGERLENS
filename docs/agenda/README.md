# Agenda (retomar luego)

Ítems que **no** entran en el demo actual. Stack vigente: parser **MinerU** `pipeline` (sidecar CPU), Infinity, chat **Groq** `llama-3.3-70b-versatile` + Ollama fallback, embed **Voyage** nativo. Esta PC = Windows Ryzen 8500G 32 GB, **sin NVIDIA**.

Consultá un archivo, no todos. Cada uno tiene disparador, checklist y dumps en `research/`.

Ítems cerrados o rechazados: [descartado.md](descartado.md).

## Quick path

1. Abrí el ítem que vas a retomar.
2. Confirmá el disparador (grafo, GPU, chrome UI, LinkedIn).
3. Seguí el checklist. No implementar sin disparador.

## Activo

| Ítem | Cuándo retomarlo |
|------|------------------|
| [vLLM](vllm.md) | GPU NVIDIA: chat local o MinerU hybrid. |
| [Posicionamiento LinkedIn](posicionamiento-linkedin.md) | Publicar tesis IDP 2026 sin vender hybrid/KG no shipped. |
| [Branding cosmético UI](branding-cosmetic.md) | Chrome LedgerLens (logo, nombre, pie Apache-2.0) sin fork. |

## Ya hecho (no es agenda)

| Tema | Estado |
|------|--------|
| Overlay **Docling Graph** | En el demo, no en `up.sh` ([nota](docling-graph.md)); 1T26/2T26 oro OK |
| Parser **MinerU** `pipeline` | Default del demo ([nota](mineru-pipeline.md)); sidecar `mineru-api:8000` |
| Chat **Groq** | Default del demo: `llama-3.3-70b-versatile`; OpenRouter Nano `:free` no es el default |
| Embed Voyage | Nativo v0.26.4 en RAGFlow (`VOYAGE_API_KEY` en la UI) |
| Parser Naive | Fallback ([nota](naive-parser.md)); DeepDoc si escaneo |
| E2E Windows 32 GB | Compose + BYMA 1T26 (comunicado, EEFF, presentación) |
| Infinity | En el repo |
| PaddleOCR opcional | Profile `paddleocr` (no es el parser extra) |
| Ollama `qwen2.5:1.5b` | Último fallback de chat, no default |
| Tests | `./scripts/check.sh` |

## Next step

Corpus BYMA en `docs/archivos_muestra/` parseado con MinerU en **`demo_4`** ([runbook](mineru-pipeline.md)). Chat default: Groq `llama-3.3-70b-versatile` (`chat_demo_4`). Después: [branding](branding-cosmetic.md) **o** [LinkedIn](posicionamiento-linkedin.md). No retomar TEI ni compose en el Linux de 7 GB. Hybrid MinerU = GPU + RAGFlow que liste el backend.
