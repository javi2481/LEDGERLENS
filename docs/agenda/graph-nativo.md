# Gancho nativo para Graph (siguiente investigación)

Graph vs Knowledge Graph de RAGFlow **ya está cerrado**. No reinvestigar eso. El overlay ya alimenta el chat (`push_hechos.py`). Falta cómo se **elige** y se **engancha** sin parecer un script suelto.

Visión (concepto, sin código todavía): orquestador entre parse DONE y chat-ready.

1. **Catálogo** de templates + descripción en lenguaje natural; matching semántico (verificar si Ontology-Based Templates existe en RAGFlow **v0.26.4** instalada).
2. **Umbral** sesgado arriba: un falso positivo (forzar `EeffByma` en un legal) es peor que un falso negativo.
3. **Trazabilidad:** template, score, versión, **página/posición** para Show Quote.

Grano: **página/sección**, no el PDF entero. Idempotencia si se reparsea.

## Pregunta para pegar mañana

> El overlay Docling Graph ya extrae consolidado vs controlante en la página 4 de EEFF BYMA y `push_hechos.py` inyecta fichas como chunk manual en el PDF (Show Quote cita el filing). No quiero más teoría Graph vs KG RAGFlow.
>
> Investigá el **gancho de ingest** vs alternativa, sobre RAGFlow **v0.26.4** pinneada:
>
> 1. ¿Docling Graph actual hace matching de catálogo/página, o el matching se arma afuera (scripts LedgerLens)?
> 2. En esta versión: ingestion pipeline vs poll API vs webhook. ¿`add_chunk` puede llevar positions de la página 4 para Show Quote?
> 3. Alternativa: JSON schema sobre el markdown MinerU de esa página vs Graph. ¿Qué se pierde en provenance / `graph_id_fields`?
>
> Criterios: no Generate KG; no reparsear MinerU; no meter Graph en Compose/`up.sh`; umbral no-inventar; idempotencia. Dump en `research/` si usás Parallel.

Dump previo: `research/search-ragflow-native-row-identity.json`.

## Qué no tocar

- Los 10 PDFs BYMA ya parseados en Windows (`demo_4`).
- Plantilla `templates/eeff_byma.py` (`graph_id_fields=["hecho_id"]`).
- Oro de página 4 (cifras en [docling-graph.md](docling-graph.md)).
