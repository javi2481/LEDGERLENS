# Claimprint

Formerly **LedgerLens**.

**Category:** Claims Intelligence  
**Instance:** BYMA financial statements  
**Rule:** no claim, no answer.

The document produces verifiable claims. This repo ships the finance plugin over the BYMA corpus in [`docs/archivos_muestra/`](docs/archivos_muestra/). Recipes + [`evals/`](evals/) define the figures; the RAGFlow chat consumes them and is **not** the source of truth. Clone and run `idp_ask` with no Docker and no API keys. Retrieval Recall@5 is 0.25 (n=20); grounded chat answer is 0.6 (n=10).

![De PDF a claim verificado](docs/assets/architecture.svg)

![Trampa consolidado vs controlante 1T26](docs/assets/identity-trap.svg)

![Retrieval empatado vs chat anclado](docs/assets/retrieval-vs-chat.svg)

**Al clonar** traés los PDF y el texto parseado en [`fixtures/mineru/`](fixtures/mineru/). Podés preguntar cifras con [`scripts/idp_ask.py`](scripts/idp_ask.py) **sin API keys y sin Docker**.

El chat en RAGFlow es una **demo de UI opcional** (PC ≥16 GB + **tus** keys). `.env` no está en git.

## Quick path (lo que ofrezco al clonar)

```bash
git clone https://github.com/javi2481/claimprint.git
cd claimprint
uv venv && uv pip install -r requirements-dev.txt
./scripts/check.sh
python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"
# → 21262335
python scripts/idp_ask.py "¿Cuál es la fecha del comunicado de prensa 1T26?"
# → 2026-05-08
python scripts/idp_ask.py "¿Cuál es el EBITDA de la presentación 1T26?"
# → 72128
python scripts/idp_ask.py "¿Cuál es el margen EBITDA LTM del comunicado de prensa 1T26?"
# → 76
python scripts/review_pack.py   # outputs/review.html (HITL)
python scripts/informe.py       # outputs/dossier.html
```

En Windows usá Git Bash o WSL para `./scripts/check.sh`.

## Qué trae el clone / qué no

| Trae | No trae |
|------|---------|
| PDF en `docs/archivos_muestra/` | Volúmenes Docker |
| Texto parseado en `fixtures/mineru/` | Dataset `demo_4` indexado |
| recipes, `evals/`, pytest | API keys (Groq, Voyage, …) |
| `scripts/idp_ask.py`, HITL, dossier | Chunks / chat listo en la UI |

## Capas y pruebas

| Capa | Qué es | Cómo se prueba |
|------|--------|----------------|
| **IDP** | fixtures → classify → extract → claims → `idp_ask` | `./scripts/check.sh` (cualquier PC) |
| **RAG** | RAGFlow + Infinity + Voyage + Groq; `demo_4` | Opcional, ≥16 GB (apéndice abajo) |

Contrato: `recipes/financial_statement.json` + `press_release.json` + `results_presentation.json` + [`evals/identity_v1.json`](evals/identity_v1.json) + [`identity_v2.json`](evals/identity_v2.json) + [`press_v1.json`](evals/press_v1.json) + [`presentation_v1.json`](evals/presentation_v1.json).

Trampas: sin decir controlante → consolidado. Neto/impuesto **del comunicado** o **de la presentación** → abstain. EBITDA en millones es de la **presentación**; margen LTM `76`/`75` está en **comunicado y presentación**. YPF / memoria → abstain.

Catálogo: **cuatro capas** (archivos → identidad → inject mock → RAG vivo). Detalle: [docs/testing.md](docs/testing.md). Cierre de planta: [docs/cierre-academico.md](docs/cierre-academico.md). Handoff: [docs/handoff-linux.md](docs/handoff-linux.md).

## Repo

| Path | Rol |
|------|-----|
| `schemas/` / `recipes/` / `evals/` | Identidad tipada |
| `fixtures/mineru/` | Parse durable (texto de identidad) |
| `scripts/idp_ask.py` | Lookup; cache en `outputs/claims.json` |
| `scripts/check.sh` | Contratos + pytest |
| `scripts/review_pack.py` / `informe.py` | HITL y dossier académico |
| `docs/archivos_muestra/` | PDFs BYMA |
| `scripts/up.sh` / `push_claims.py` | Solo si armás el stack RAG |
| `vendor/ragflow-docker/` | Pin RAGFlow v0.26.4 (no editar) |
| `docs/assets/` | Diagramas del README / LinkedIn |

---

## Apéndice: UI RAGFlow (opcional, ≥16 GB)

**No es el first-run.** Sirve para ver el chat sobre el mismo corpus. Necesitás Docker, Compose y **tus propias** keys (Groq + Voyage). El clone no trae `demo_4` indexado.

Stack: **RAGFlow** v0.26.4 + Infinity. Parser **MinerU** `pipeline`. Chat **Groq** `llama-3.3-70b-versatile` (Ollama fallback). Embed **Voyage**. PaddleOCR apagado por defecto.

### Requisitos

| Requisito | Valor |
|-----------|--------|
| Arquitectura | **x86_64** (no ARM64) |
| RAM | **≥ 16 GB** (32 GB recomendado) |
| Disco | ≥ 50 GB |
| Docker | ≥ 24.0.0, Compose ≥ v2.26.1 |
| Kernel | `vm.max_map_count` ≥ 262144 |

```bash
cp .env.example .env   # pegá keys; .env no está en git
./scripts/check.sh
./scripts/up.sh        # UI: http://localhost
```

RAGFlow **no** lee las keys solo: pegá Groq y Voyage en Model providers. Ollama: `http://host.docker.internal:11434` (**nunca** `127.0.0.1` desde el contenedor).

| Pieza | Default | Fallback |
|-------|---------|----------|
| UI + RAG | RAGFlow v0.26.4 :80 | — |
| Motor docs | Infinity | no Elasticsearch |
| Parser PDF | MinerU `pipeline` | Naive; DeepDoc; PaddleOCR (profile) |
| Chat | Groq `llama-3.3-70b-versatile` | Ollama `qwen2.5:1.5b` |
| Embeddings | Voyage `voyage-finance-2` | Gemini `gemini-embedding-001` |

### Primera vez en la UI

1. Registro local.
2. Model providers: Groq + Voyage (+ MinerU vía `MINERU_APISERVER`).
3. Knowledge base **`demo_4`**: parser MinerU, español, KG/RAPTOR off. Subir `docs/archivos_muestra/*.pdf`. Page size **128**. Parse de a uno. Runbook: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).
4. Asistente **`chat_demo_4`**, Show Quote on, umbral **0.3**. Luego `python scripts/push_claims.py` y un **chat nuevo**.

```text
Claimprint
 ├── IDP   classify → extract → lookup → pytest
 └── RAG   RAGFlow → Infinity (BM25 + dense + hybrid) → Groq
```

Infinity puntúa full-text con **BM25**. Los brazos `keyword` / `vector` / `hybrid` son knobs de RAGFlow (`vector_similarity_weight` 0 / 1 / 0.3), no una librería Okapi propia. Knobs del piloto (rerank off): similarity threshold `0.3`, vector weight `0.3`.

Métricas medidas (n=20 retrieval; n=10 chat). **No** inventar Recall.

| Brazo | Recall@5 | Recall@10 | MRR |
|-------|----------|-----------|-----|
| keyword | 0.25 | 0.25 | 0.125 |
| vector | 0.25 | 0.25 | 0.125 |
| hybrid | 0.25 | 0.25 | 0.125 |

Los tres brazos empatan: el piloto **no** demuestra que hybrid gane. El chat da retrieval **0.7** / answer **0.6** / citation **0.7** / abstention **0.7** porque `push_claims` ancla las cifras del IDP. Dumps en `outputs/` (gitignored).

Parar el stack:

```bash
docker compose --env-file .env \
  -f vendor/ragflow-docker/docker-compose.yml \
  -f docker-compose.overlay.yml down -v
```

---

## OpenSpec y licencia

SDD activo: [`ledgerlens-rag-pilot`](openspec/changes/ledgerlens-rag-pilot/). Pin de UI/stack (no inflar con IDP): [`ledger-lens-ragflow`](openspec/changes/ledger-lens-ragflow/).

Claimprint (código propio) es **Apache-2.0**; ver [`LICENSE`](LICENSE). RAGFlow `docker/` se redistribuye bajo Apache-2.0. Claimprint no modifica esos archivos.
