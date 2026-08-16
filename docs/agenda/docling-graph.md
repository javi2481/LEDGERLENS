# Docling Graph — overlay de hechos (agenda)

No es un parser de RAGFlow. Convierte documentos (vía Docling) en objetos **Pydantic** validados y un grafo dirigido **NetworkX**: emisor, período, estado (controlante vs consolidado), métrica, unidad, hecho, ancla.

PyPI **docling-graph 1.9.1** (17 jul 2026). MIT. IBM / LF. Docs: [docling-graph](https://docling-project.github.io/docling-graph/). Repo: [github.com/docling-project/docling-graph](https://github.com/docling-project/docling-graph).

En finanzas y legal el punto es **conexiones exactas**, no embeddings aproximados. El chat RAGFlow (vectores) se queda; Graph es comparación + evidencia.

Dumps: `research/extract-docling-graph-docs.json`, `research/extract-docling-graph-config.json`, `research/search-docling-graph.json`, `research/deep-docling-graph-vllm-market.json`.

## Quick path (esta PC, sin GPU)

1. `pip install docling-graph` (LiteLLM ya viene). No hace falta extra `vlm`.
2. Plantilla Pydantic estrecha: emisor, período, estado, métrica, unidad, fuente (página).
3. `backend="llm"`, `inference="remote"` (Groq / Gemini / OpenRouter / Mistral). Misma key que el demo, no commitear.
4. Opcional: `docling_serve_url` al sidecar de [docling-serve.md](docling-serve.md) para no cargar modelos de conversión en el cliente.
5. `extraction_contract="dense"` en EEFF largos. `provenance="standard"` (default, cero tokens extra).

## Details

| Tema | Decisión |
|------|----------|
| Disparador | Hace falta comparar períodos / controlante vs consolidado sin que el vector mezcle filas |
| Esta PC | LLM **remoto**. VLM de Graph es solo local + GPU → no |
| Conversión | Local Docling o Docling Serve. `docling_config="ocr"` (clásico), no `"vision"` |
| Merge | `docling-graph merge`: fusionar EEFF + hechos relevantes **sin** LLM |
| Export | JSON / CSV / Cypher. Provenance en `__provenance__` |
| Hardware Graph | Mín. 8 GB RAM; GPU solo si inference local o VLM |
| No es | Reemplazo del dataset RAGFlow. No va en `up.sh` |

Ejemplo de config (remoto):

```python
config = PipelineConfig(
    source="eef.pdf",
    template="templates.EeffByma",  # nuestra plantilla
    backend="llm",
    inference="remote",
    processing_mode="many-to-one",
    extraction_contract="dense",
    provenance="standard",
)
```

Local GPU (después): `inference="local"`, `provider_override="vllm"`, `model_override="ibm-granite/granite-4.0-1b"` — ver [vllm.md](vllm.md).

## Checklist

- [ ] Plantilla EEFF con `graph_id_fields` estables (CUIT + período + estado)
- [ ] Un run remoto sobre el EEFF BYMA; nodos con página
- [ ] No mezclar demo_1 Gemini con vectores Voyage
- [ ] No vender Graph en LinkedIn como shipped hasta ese run

## Next step

Plantilla mínima + un PDF. Serve puede venir después.
