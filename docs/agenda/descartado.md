# Descartado (no retomar)

Decisiones 2026-08-15. Los dumps en `research/` se quedan como archivo; estos ítems **no** vuelven a la agenda activa.

| Ítem | Por qué se descarta |
|------|---------------------|
| **MinerU** | Un solo parser extra: Docling Serve CPU. RAGFlow es cliente remoto de MinerU (otro servidor GPU/API). No aporta vs Docling en este demo. |
| **OpenDataLoader** | Mismo criterio. Experimental en RAGFlow; no es el bakeoff. |
| **TEI embeddings locales** | El embed del demo es **Voyage** (nativo v0.26.4). TEI era el plan B cuando OpenRouter embed falló; no se eligió. Otro servicio + re-embed. Profile `tei-*` del vendor no se enciende. Dump: `research/stack-embeddings-cloud.json`. |
| **E2E host ≥16 GB (Linux ~7 GB)** | Esa máquina no es el compose. El demo vive en **Windows 32 GB**; E2E BYMA 1T26 ya cerró. No forzar RAGFlow en 7,4 GB. |
| **Nemotron Ultra 550B `:free`** | Inestable / rate-limit para demo. Nano cubre el E2E. Lightning tampoco se agenda: si Nano no alcanza, se prueba en el momento, no como ítem. Dump: `research/stack-openrouter-nvidia-free.json`. |
| **Xinference / GPUStack / SGLang** | Alternativas locales a vLLM. Un runtime GPU basta; el diferido es solo vLLM. Dump: `research/stack-ollama-vllm-local.json`. |
| **PaddleOCR como “próximo parser”** | El profile `paddleocr` **sigue en el repo**. No es el experimento de tablas (eso es Docling). No borrar el profile. |
| **Parser VLM / Granite-Docling en esta APU** | 258M existe; vLLM pide NVIDIA (`--revision untied`). Ollama 258M es experimento, no ítem de agenda. |

Archivos que había en esta carpeta y se eliminaron: `mineru-docling.md`, `tei-embeddings.md`, `e2e-16gb.md`, `openrouter-larger-models.md`.
