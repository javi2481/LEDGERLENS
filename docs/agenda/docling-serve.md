# Docling Serve — no es el parser default

Quedó fuera del demo: el cliente Docling de RAGFlow v0.26.4 no manda `page_range` ([issue #17450](https://github.com/infiniflow/ragflow/issues/17450)). Parser vigente: [mineru-pipeline.md](mineru-pipeline.md).

Docling clásico (Heron + TableFormer, no Granite-Docling VLM) puede volver si InfiniFlow mergea el PR. Graph de hechos sigue en agenda y **no** es el parser: [docling-graph.md](docling-graph.md).

Sidecar Compose `docling-serve` ya no está en [docker-compose.overlay.yml](../../docker-compose.overlay.yml). No setear `DOCLING_SERVER_URL`. `USE_DOCLING=false` (no in-process).

Dumps: `research/extract-docling-classic-vlm.json`, `research/search-docling-classic-parser.json`.
