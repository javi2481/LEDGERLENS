# Agenda (retomar luego)

Ítems que **no** entran en el demo actual. Stack vigente: parser **Docling** clásico (sidecar CPU), Infinity, chat OpenRouter Nano (`:free`) + Gemini, embed **Voyage**, Ollama fallback. Esta PC = Windows Ryzen 8500G 32 GB, **sin NVIDIA**.

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
| [vLLM](vllm.md) | GPU NVIDIA: chat, Granite-Docling VLM, o LLM local de Graph. |
| [Posicionamiento LinkedIn](posicionamiento-linkedin.md) | Publicar tesis IDP 2026 sin vender Graph/VLM no shipped. |
| [Branding cosmético UI](branding-cosmetic.md) | Chrome LedgerLens (logo, nombre, pie Apache-2.0) sin fork. |

## Ya hecho (no es agenda)

| Tema | Estado |
|------|--------|
| Parser **Docling** clásico | Default del demo ([nota](docling-serve.md)); sidecar `docling-serve:5001` |
| Parser Naive | Fallback ([nota](naive-parser.md)); DeepDoc si escaneo |
| E2E Windows 32 GB | Compose + BYMA 1T26 (comunicado, EEFF, presentación) |
| Infinity | En el repo |
| PaddleOCR opcional | Profile `paddleocr` (no es el parser extra) |
| OpenRouter chat Nano | Default; Gemini también cableado |
| Embed Voyage | Nativo v0.26.4 (`VOYAGE_API_KEY` en `.env`) |
| Ollama `qwen2.5:1.5b` | Fallback, no default |
| Tests | `./scripts/check.sh` |

## Next step

Corpus BYMA en `docs/archivos_muestra/` con parser Docling (re-parse de lo que quedó en Naive). Después: [plantilla Graph](docling-graph.md) **o** [branding](branding-cosmetic.md) **o** [LinkedIn](posicionamiento-linkedin.md). No retomar TEI, MinerU ni compose en el Linux de 7 GB.
