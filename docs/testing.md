# Pruebas LedgerLens

El contrato de identidad es extract + lookup, exact-match, sin embeddings. `./scripts/check.sh` corre contratos de archivos **y** `pytest tests/`. El chat RAGFlow se prueba a mano en ≥16 GB; **no** sustituye al IDP.

## Oro

El único oro de cifras es recipes + `evals/identity_v1.json` + `identity_v2.json` + `press_v1.json` + `presentation_v1.json`. Pytest extrae desde `fixtures/mineru/`. CLI: `idp_ask.py` usa `outputs/claims.json`. El inject (`scripts/push_claims.py`) **genera** fichas desde esos claims; no hay un JSON gemelo.

## Promesa IDP

Ningún test de identidad llama a RAGFlow.

| Caso | Pregunta | Debe devolver | Debe rechazar |
|------|----------|---------------|---------------|
| 1T26 trampa | ¿Cuál es el resultado neto del período 1T26? | **21262335** | 21259769 y 22362983 |
| 1T26 controlante | ¿Resultado atribuible a la participación controlante 1T26? | **21259769** | el consolidado |
| 2T26 trampa | Resultado neto del período 2T26 (sin decir consolidado) | **81956525** | 81946993 |
| Fuera de corpus | ¿Precio de cierre de YPF en BYMA el 3 de enero? | abstain | cifra inventada |
| 1T26 bruto | ¿Cuál es el resultado bruto del 1T26? | **60144176** | operativo y neto |
| 1T26 impuesto | ¿Impuesto a las ganancias 1T26? | **-14950948** | el neto |
| 1T26 EBITDA deck | ¿Cuál es el EBITDA de la presentación 1T26? | **72128** | neto del EEFF |
| 1T26 LTM comunicado | ¿Cuál es el margen EBITDA LTM del comunicado de prensa 1T26? | **76** | 72128 y 75 |
| EBITDA sin LTM del comunicado | ¿Cuál es el EBITDA del comunicado 1T26? | abstain | 76 o 72128 |

## Qué corre en CI

`scripts/check.sh`: pin vendor, overlay MinerU, `.env.example`, PDFs + fixtures, pytest (incluye mock HTTP de `push_claims`). Probe de RAM/Docker es **SKIP**, no FAIL, en hosts <16 GB.

## Chat (manual, ≥16 GB)

`./scripts/up.sh`, dataset `demo_4`, `python scripts/push_claims.py`, chat **nuevo**: neto 1T26, controlante, empty YPF, Show Quote al PDF del EEFF.

Retrieval: Infinity es **hybrid keyword + vector** (no Okapi BM25). Piloto: [`evals/retrieval_v1.json`](../evals/retrieval_v1.json) (20 qrels de PDF+página) y [`evals/rag_chat_v1.json`](../evals/rag_chat_v1.json) (10 preguntas). `python scripts/retrieval_bench.py` y `python scripts/rag_eval.py` hacen skip sin stack. Recall@k se pega en el README **después** del run en ≥16 GB; no inventar números. Detalle: [cierre-academico.md](cierre-academico.md).

HITL: `python scripts/review_pack.py`. Dossier: `python scripts/informe.py`. Un `reject` no sale en hechos publicados.
