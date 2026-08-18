# Descartado (no retomar)

Decisiones 2026-08-15, actualizado 2026-08-16. Los dumps en `research/` se quedan como archivo; estos ítems **no** vuelven a la agenda activa.

| Ítem | Por qué se descarta |
|------|---------------------|
| **Parser extra en RAGFlow (no MinerU)** | El demo usa [MinerU pipeline](mineru-pipeline.md). No hay sidecar de conversión aparte en el overlay. |
| **OpenDataLoader** | Experimental en RAGFlow; no es el bakeoff. Un solo parser extra: MinerU. |
| **TEI embeddings locales** | El embed del demo es **Voyage** (nativo v0.26.4). TEI era el plan B cuando OpenRouter embed falló; no se eligió. Otro servicio + re-embed. Profile `tei-*` del vendor no se enciende. Dump: `research/stack-embeddings-cloud.json`. |
| **E2E host ≥16 GB (Linux ~7 GB)** | Esa máquina no es el compose. El demo vive en **Windows 32 GB**; E2E BYMA 1T26 ya cerró. No forzar RAGFlow en 7,4 GB. |
| **Nemotron Ultra 550B `:free` / Nano `:free`** | Inestable / rate-limit para demo. El E2E vive corre en Groq `llama-3.3-70b-versatile`. Dump: `research/stack-openrouter-nvidia-free.json`. |
| **Xinference / GPUStack / SGLang** | Alternativas locales a vLLM. Un runtime GPU basta; el diferido es solo vLLM. Dump: `research/stack-ollama-vllm-local.json`. |
| **PaddleOCR como “próximo parser”** | El profile `paddleocr` **sigue en el repo**. No es el experimento de tablas (eso es MinerU). No borrar el profile. |
| **Parser VLM en esta APU** | Pide NVIDIA. Ollama VLM es experimento, no ítem de agenda. |
| **Overlay de hechos / grafo (como ítem “sin código”)** | Superado: el overlay está en `main` ([nota](docling-graph.md)). Lo que falta es el gancho de ingest ([graph-nativo.md](graph-nativo.md)), no reabrir “hay Graph o no”. |
| **MinerU hybrid en esta APU** | `hybrid-engine` no corre en CPU; RAGFlow v0.26.4 no lista el backend. Agenda: [vllm.md](vllm.md) cuando haya NVIDIA. |
| **Proxy extra de chat (Compose)** | Innecesario para este demo: RAGFlow ya elige Groq / Ollama / Voyage en Model providers. El hop extra no aportaba. |

Archivos que había en esta carpeta y se eliminaron: `mineru-docling.md`, `tei-embeddings.md`, `e2e-16gb.md`, `openrouter-larger-models.md`, `litellm.md`, `docling-graph.md`, `docling-serve.md`.
