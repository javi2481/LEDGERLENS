# LedgerLens

IDP **financiero** de punta a punta sobre [`docs/archivos_muestra/`](docs/archivos_muestra/) (BYMA). Un parse MinerU alimenta dos capas: claims tipados (identidad) y chat RAGFlow (uso). Las cifras las define el IDP (`evals/` + recipes). El chat las consume; no es la fuente de verdad.

## Capas

| Capa | Qué es | Cómo se prueba |
|------|--------|----------------|
| **IDP** | `fixtures/mineru/*.md` → classify → extract → claims → [`scripts/idp_ask.py`](scripts/idp_ask.py) | `./scripts/check.sh` (cualquier PC; sin Docker) |
| **RAG** | RAGFlow v0.26.4 + Infinity + Voyage + Groq; dataset `demo_4` | PC ≥16 GB, `./scripts/up.sh`. Eval de chat: manual |

SDD activo: [`ledgerlens-results-presentation`](openspec/changes/ledgerlens-results-presentation/). Shipped: kernel, P&L, claim-store, press-release, mineru-parse, product-shape, claims-to-rag. Pin de UI/stack (no inflar con trabajo IDP): [`ledger-lens-ragflow`](openspec/changes/ledger-lens-ragflow/).

Contrato de identidad: `recipes/financial_statement.json` + `recipes/press_release.json` + `recipes/results_presentation.json` + [`evals/identity_v1.json`](evals/identity_v1.json) + [`evals/identity_v2.json`](evals/identity_v2.json) + [`evals/press_v1.json`](evals/press_v1.json) + [`evals/presentation_v1.json`](evals/presentation_v1.json). El chat no define cifras: `python scripts/push_claims.py` inyecta los claims del kernel en RAGFlow. **Después de un merge, corré el push en el host de la UI y abrí un chat nuevo.**

## Quick path (IDP, cualquier PC)

1. `uv venv && uv pip install -r requirements-dev.txt`
2. `./scripts/check.sh`
3. `python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"` → `21262335`
4. `python scripts/idp_ask.py "¿Cuál es la fecha del comunicado de prensa 1T26?"` → `2026-05-08`
5. `python scripts/idp_ask.py "¿Cuál es el EBITDA de la presentación 1T26?"` → `72128`

Trampas: sin decir controlante → consolidado. Neto/impuesto **del comunicado** o **de la presentación** → abstain. EBITDA/margen LTM son de la presentación, no del EEFF. YPF / memoria → abstain. Detalle: [docs/testing.md](docs/testing.md).

## UI y stack (PC ≥16 GB, x86_64)

Stack: **RAGFlow** v0.26.4 + Infinity. Parser **MinerU** `pipeline`. Chat **Groq** `llama-3.3-70b-versatile` + Ollama fallback. Embed **Voyage**. **PaddleOCR** apagado por defecto.

1. Docker ≥24, **Compose v2**, usuario en `docker`, `vm.max_map_count` ≥ 262144.
2. Copiar `.env.example` → `.env`. Pegar keys (**.env no está en git**).
3. `./scripts/check.sh` y `./scripts/up.sh`. UI: <http://localhost>
4. Groq + Voyage, dataset **`demo_4`**, parser **MinerU**, Empty response + Show Quote. Runbook: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).
5. Inject de claims: `python scripts/push_claims.py` y un **chat nuevo**. Obligatorio después de cada merge que cambie claims.

### Stack

| Pieza | Default | Fallback / opcional |
|-------|---------|---------------------|
| UI + RAG | RAGFlow **v0.26.4** puerto 80 | — |
| Motor docs | **Infinity** | no Elasticsearch |
| Parser PDF | **MinerU** `pipeline` (`MINERU_APISERVER=http://mineru-api:8000`) | Naive; DeepDoc (escaneos); PaddleOCR (profile) |
| Chat | Groq `llama-3.3-70b-versatile` | Ollama `qwen2.5:1.5b` |
| Embeddings | Voyage `voyage-finance-2` (nativo v0.26.4) | Gemini `gemini-embedding-001` |
| Empty response | `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.` | no dejar en blanco |

RAGFlow **no** lee las API keys solo: pegá Groq y Voyage en Model providers. Ollama, si lo usás: `http://host.docker.internal:11434` (**nunca** `127.0.0.1` desde el contenedor). MinerU hybrid pide GPU; no entra.

### Requisitos Compose

| Requisito | Valor |
|-----------|--------|
| Arquitectura | **x86_64** (imágenes oficiales, no ARM64) |
| RAM | **≥ 16 GB** (32 GB recomendado) |
| Disco | ≥ 50 GB |
| Docker | ≥ 24.0.0, usuario en grupo `docker` |
| Compose | ≥ v2.26.1 (`docker compose`, no el binario mailcap `compose`) |
| Kernel | `vm.max_map_count` ≥ 262144 |

```bash
cat /proc/sys/vm/max_map_count
# si es bajo, como root (no lo hace up.sh):
sudo sysctl -w vm.max_map_count=262144
```

```bash
cp .env.example .env   # luego keys
./scripts/check.sh
./scripts/up.sh
```

`up.sh` falla si `vm.max_map_count` es bajo; copia `.env` a `vendor/ragflow-docker/.env`; levanta Infinity+CPU+MinerU API; PaddleOCR queda apagado; pull de Ollama solo si está instalado.

Parar:

```bash
docker compose --env-file .env \
  -f vendor/ragflow-docker/docker-compose.yml \
  -f docker-compose.overlay.yml down -v
```

### Primera vez en la UI

1. Registro local.
2. **Model providers:** Groq `llama-3.3-70b-versatile`; Voyage `voyage-finance-2` + `rerank-2.5-lite`; MinerU vía `MINERU_APISERVER`.
3. Knowledge base **`demo_4`**: Configuración primero (PDF parser = **MinerU**; español; Knowledge graph y RAPTOR off). Después subir `docs/archivos_muestra/*.pdf`. En cada file, **Tamaño de la tarea por página = 128**. Parse de a uno. Runbook: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).
4. Asistente **`chat_demo_4`**, KB tildada, **Show Quote** on, umbral **0.3**, Empty response no vacío. Luego `python scripts/push_claims.py` y un chat nuevo.

Ollama en el host, si lo usás:

```bash
export OLLAMA_HOST=0.0.0.0
ollama pull qwen2.5:1.5b
```

PaddleOCR opcional: `COMPOSE_PROFILES=infinity,cpu,paddleocr`. Naive/DeepDoc solo si MinerU no corre o el PDF es escaneo.

## Repo

| Path | Rol |
|------|-----|
| `schemas/` / `recipes/` / `evals/` | Identidad tipada |
| `fixtures/mineru/` | Parse durable (texto de identidad) |
| `scripts/export_mineru.py` | Export `demo_4` → fixtures (host con stack) |
| `scripts/idp_ask.py` | Lookup; cache en `outputs/claims.json` |
| `openspec/changes/ledgerlens-product-shape/` | SDD activo |
| `vendor/ragflow-docker/` | Pin v0.26.4. No editar. [vendor/PIN.md](vendor/PIN.md) |
| `docker-compose.overlay.yml` / `docker/mineru/` | Sidecar MinerU |
| `scripts/up.sh` | Arranque Compose |
| `scripts/push_claims.py` | Inject de claims al chat (correr tras merge, chat nuevo) |
| `openspec/changes/ledger-lens-ragflow/` | Pin de UI/stack |
| `scripts/check.sh` | Contratos + pytest |
| `docs/archivos_muestra/` | PDFs BYMA |
| `docs/agenda/mineru-pipeline.md` | Runbook de parse |

Producto: actualizar `README.md` y el change OpenSpec **abierto** en el mismo trabajo (hoy: [ledgerlens-results-presentation](openspec/changes/ledgerlens-results-presentation/)). El pin y `.env.example` solo si cambia el stack.

## Licencia del vendor

RAGFlow `docker/` se redistribuye bajo Apache-2.0. LedgerLens no modifica esos archivos.
