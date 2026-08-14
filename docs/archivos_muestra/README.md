# Muestras BYMA (E2E local)

PDFs reales de BYMA 1T26 para probar RAGFlow en esta PC. No son los fixtures sintéticos de `examples/synthetic/` (Acme Norte).

| Archivo | Qué es |
|---------|--------|
| `BYMA_Comunicado_de_Prensa-Resultados-1T26.pdf` | Comunicado 8 de mayo de 2026 |
| `BYMA_-_EEFF_31-03-2026_VF.pdf` | EEFF condensados al 31-03-2026 (~80 págs.; embed Gemini free puede dar 429 RPM) |
| `Presentación_de_resultados_BYMA-1T26.pdf` | Slides 1T26 |

Dataset UI usado: `demo_1`. Parser **Naive**. Chat: OpenRouter `nvidia/nemotron-3-nano-30b-a3b:free`. Embed: Gemini `gemini-embedding-001`.
