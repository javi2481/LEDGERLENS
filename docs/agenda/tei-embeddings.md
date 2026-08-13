# TEI embeddings locales (agenda)

RAGFlow vendor ya trae servicios `tei-cpu` / `tei-gpu` (profile). Modelos: `Qwen/Qwen3-Embedding-0.6B`, `BAAI/bge-m3`, `BAAI/bge-small-en-v1.5`. Docs: [Configuration](https://ragflow.io/docs/configurations).

No activar en esta PC (~7,4 GB). OpenRouter embed es el default.

## Quick path

1. Host ≥16 GB (mejor GPU).
2. `COMPOSE_PROFILES` + profile `tei-cpu` o `tei-gpu`.
3. Model providers → TEI / HuggingFace embeddings. Re-embed del dataset.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | Demo offline o sin cuota OpenRouter |
| Rechazado ahora | RAM extra vs cloud gratis |
| Dump | `research/stack-embeddings-cloud.json` |
| Vendor | `vendor/ragflow-docker/docker-compose-base.yml` (`tei-cpu`) |

## Checklist

- [ ] Profile TEI no se enciende en el default de `.env.example`
- [ ] Dataset re-indexado (cambiar embed obliga a re-embed)
- [ ] Retrieval E2E sigue citando los PDFs sintéticos

## Next step

Solo si OpenRouter embed falla o el demo debe ser 100 % local.
