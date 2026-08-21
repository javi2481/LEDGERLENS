# Pruebas Claimprint

Claimprint no tiene once suites paralelas. Tiene **cuatro capas**. La taxonomía QA (unit, E2E, security, load, ML, etc.) se mapea a esas capas; no se inventan carpetas `tests/unit|e2e|security|load`.

El contrato de identidad es extract + lookup, exact-match, sin embeddings. El chat RAGFlow **no** sustituye al IDP. First-run del repo: capas 1–2 vía `./scripts/check.sh` e `idp_ask` (sin keys); capa 4 es el runbook de [cierre-academico.md](cierre-academico.md). El README resume las métricas del piloto.

## Cuatro capas

| Capa | Qué prueba | Cómo | Host |
|------|------------|------|------|
| **1. Archivos** | Pin vendor, overlay MinerU, recetas, evals presentes, secrets fuera de git | [`scripts/check.sh`](../scripts/check.sh) | Cualquiera |
| **2. Identidad** | Cifras exactas (neto, controlante, LTM, abstain) | `pytest tests/` + [`evals/`](../evals/) | Cualquiera |
| **3. Inject** | Claims del kernel → fichas de chat (sin red) | `tests/test_push_claims.py`, `tests/test_inject.py` (HTTP mock) | Cualquiera |
| **4. RAG vivo** | Retrieval (PDF+página) + chat + trampas UI | `retrieval_bench.py`, `rag_eval.py`, trampas a mano | ≥16 GB + stack |

```text
check.sh (capa 1)
 └── pytest identidad + mock inject (capas 2–3)   ← siempre
 └── up.sh → push_claims → bench + rag_eval      ← solo ≥16 GB (capa 4)
```

### Mapeo de nombres QA → capas

| Nombre | Dónde vive aquí |
|--------|-----------------|
| Contract / smoke | Capa 1 (`check.sh`) |
| Unit / data validation / regression | Capa 2 (pytest + oro `evals/`) |
| Integration | Capa 3 (mock `push_claims`) |
| E2E / RAG evaluations / “performance” del producto | Capa 4 (Recall/MRR + chat scores) |
| Security | Asserts de `.env` en `check.sh` (no pentest) |
| Load / Model-ML eval aparte | **Fuera.** Groq es caja negra; el oro no es embeddings |

`"skipped": true` / `reason: no_ragflow` en un dump **no** cuenta como piloto corrido. Hay que medir en vivo y pegar números en el README.

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

## Qué corre en CI / cualquier PC (capas 1–3)

`scripts/check.sh`: pin vendor, overlay MinerU, `.env.example`, PDFs + fixtures, pytest (incluye mock HTTP de `push_claims`). Probe de RAM/Docker es **SKIP**, no FAIL, en hosts <16 GB.

## Capa 4 — RAG vivo (≥16 GB)

`./scripts/up.sh`, dataset `demo_4`, `python scripts/push_claims.py`, chat **nuevo**: neto 1T26, controlante, empty YPF, Show Quote al PDF del EEFF.

Retrieval: Infinity hace **full-text BM25 + dense + hybrid**. No hay una segunda librería Okapi en Python; los brazos del piloto son knobs de RAGFlow (`vector_similarity_weight` 0 / 1 / 0.3). Piloto: [`evals/retrieval_v1.json`](../evals/retrieval_v1.json) (20 qrels de PDF+página) y [`evals/rag_chat_v1.json`](../evals/rag_chat_v1.json) (10 preguntas). `python scripts/retrieval_bench.py` y `python scripts/rag_eval.py` hacen skip sin stack (exit 0). Ese skip **no** es el DoD del piloto: Recall@k se pega en el README **después** del run medido; no inventar números. Las métricas de retrieval solo y de chat post-`push_claims` **no se promedian**: son dos capas. Detalle: [cierre-academico.md](cierre-academico.md).

HITL: `python scripts/review_pack.py`. Dossier: `python scripts/informe.py`. Un `reject` no sale en hechos publicados.
