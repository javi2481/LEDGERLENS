# LedgerLens

Demo de portfolio: preguntas en **español** sobre PDFs financieros de **BYMA**, con citas. Si no hay evidencia, responde vacío (no inventa).

Stack: **RAGFlow** v0.26.4 self-host (UI + RAG) + Infinity. Parser **MinerU** `pipeline` (sidecar CPU). Chat **Groq** `llama-3.3-70b-versatile` + Ollama fallback. Embed **Voyage** nativo. **PaddleOCR** no arranca por defecto.

Corpus: `docs/archivos_muestra/` (comunicados, EEFF, presentaciones, memoria).

## Quick path (PC ≥16 GB, x86_64)

1. Instalar Docker ≥24 y **Compose v2** (`docker compose version`). Tu usuario en el grupo `docker`. `vm.max_map_count` ≥ 262144.
2. Clonar `https://github.com/javi2481/LEDGERLENS`. Copiar `.env.example` → `.env`. Pegar keys (**.env no está en git**).
3. `./scripts/check.sh` y después `./scripts/up.sh`. UI: <http://localhost>
4. En la UI: Groq `llama-3.3-70b-versatile` + Voyage embed, dataset **`demo_4`**, parser **MinerU**, Empty response + Show Quote (abajo). Runbook: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).

En una PC de ~7 GB: solo `./scripts/check.sh`. Compose + E2E: esta PC Windows 32 GB. Diferidos: [docs/agenda/](docs/agenda/).

## Stack (fuente de verdad del demo)

| Pieza | Default | Fallback / opcional |
|-------|---------|---------------------|
| UI + RAG | RAGFlow **v0.26.4** puerto 80 | — |
| Motor docs | **Infinity** | no Elasticsearch |
| Parser PDF | **MinerU** `pipeline` (`MINERU_APISERVER=http://mineru-api:8000`) | Naive; DeepDoc (escaneos); PaddleOCR (profile) |
| Chat | Groq `llama-3.3-70b-versatile` | Ollama `qwen2.5:1.5b` |
| Embeddings | Voyage `voyage-finance-2` (nativo v0.26.4) | Gemini `gemini-embedding-001` |
| Empty response | `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.` | no dejar en blanco |

RAGFlow **no** lee las API keys solo: hay que pegar Groq (`llama-3.3-70b-versatile`) y Voyage en Model providers. Ollama, si lo usás: `http://host.docker.internal:11434` (**nunca** `127.0.0.1` desde el contenedor). `USE_DOCLING=false`. No setear `DOCLING_SERVER_URL`. MinerU hybrid / Granite-Docling VLM no entran en este demo. No hay sidecar LiteLLM. OpenRouter Nano `:free` no es el default (cuota).

## Requisitos

| Requisito | Valor |
|-----------|--------|
| Arquitectura | **x86_64** (imágenes oficiales, no ARM64) |
| RAM | **≥ 16 GB** (32 GB recomendado: RAGFlow + MinerU pipeline CPU) |
| Disco | ≥ 50 GB |
| Docker | ≥ 24.0.0, usuario en grupo `docker` |
| Compose | ≥ v2.26.1 (`docker compose`, no el binario mailcap `compose`) |
| Kernel | `vm.max_map_count` ≥ 262144 |

```bash
cat /proc/sys/vm/max_map_count
# si es bajo, como root (no lo hace up.sh):
sudo sysctl -w vm.max_map_count=262144
```

## Arranque

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

## Primera vez en la UI

1. Registro local.
2. **Model providers**
   - **Groq:** `llama-3.3-70b-versatile` (chat default). Pegá `GROQ_API_KEY` en la factory.
   - Voyage: `voyage-finance-2` (embed) y `rerank-2.5-lite`.
   - MinerU: auto-provision con `MINERU_APISERVER` en `.env`, o agregarlo a mano.
   - Ollama (fallback): `http://host.docker.internal:11434`, modelo `qwen2.5:1.5b`. No uses OpenRouter Nano `:free` ni un proxy LiteLLM.
3. Knowledge base **`demo_4`**: **Configuración primero** (PDF parser = **MinerU**; español; Knowledge graph y RAPTOR off). **Después** subir `docs/archivos_muestra/*.pdf`. En cada file, **Tamaño de la tarea por página = 128**. **Por último** Parse, de a uno. Si MinerU está caído, el ingest debe fallar visible (no texto inventado). Cambiar Configuración no pisa archivos ya subidos. Detalle: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).
4. Chat en español: asistente **`chat_demo_4`**, KB tildada, **Show Quote** on, umbral **0.3** (Voyage rerank; 0.4 devolvía 0 chunks), Empty response no vacío (copy de la tabla de stack). Prompt: *Responde solo en español. Cita los fragmentos. Si no hay evidencia, usa la respuesta vacía. No inventes cifras.*

Ollama en el host, si lo usás:

```bash
export OLLAMA_HOST=0.0.0.0
ollama pull qwen2.5:1.5b
```

## Checklist E2E

Con `ragflow-cpu` en :80, `mineru-api` healthy y Voyage configurado:

1. Ingest MinerU de los PDFs de `docs/archivos_muestra/` (empezar por comunicados; EEFF y Memoria al final).
2. *¿Cuál es el RESULTADO NETO DEL PERÍODO consolidado del EEFF?* → español + Show Quote (número del PDF, no inventado).
3. *¿Cuál fue el precio de cierre de YPF en BYMA el 3 de enero?* → Empty response, sin inventar.

Un clone de GitHub **no** trae chunks: Infinity/MySQL/MinIO viven en volúmenes Docker. Quien pruebe el repo parsea en su máquina. El parseo previo es de **esta instancia** (demo LinkedIn / screenshots).

## Opcional: Naive / DeepDoc / PaddleOCR

MinerU es el default para EEFF con tablas. Naive si el API no está. DeepDoc si no hay capa de texto. PaddleOCR: `COMPOSE_PROFILES=infinity,cpu,paddleocr`, descomentar vars en `.env`, factory `http://paddleocr:8080/layout-parsing`, `PP-StructureV3`, token vacío.

## Repo

| Path | Rol |
|------|-----|
| `vendor/ragflow-docker/` | Pin oficial v0.26.4. No editar. [vendor/PIN.md](vendor/PIN.md) |
| `docker-compose.overlay.yml` | MinerU API CPU + PaddleOCR opcional, sin `:8080` |
| `docker/mineru/` | Sidecar `mineru[pipeline]==3.4.5`, `mineru-api :8000` |
| `.env.example` | Infinity + pin; `MINERU_APISERVER`; `GROQ_API_KEY` comentado; PaddleOCR comentado |
| `scripts/up.sh` / `scripts/check.sh` | Arranque / contratos+PDFs |
| `docs/archivos_muestra/` | PDFs BYMA del demo |
| `docs/agenda/` | Diferidos (Graph, vLLM, branding, LinkedIn) |
| `research/` | Dumps Parallel |
| `openspec/changes/ledger-lens-ragflow/` | SDD activo (Gentle AI hybrid) |

No hay `app.py`, `ledger_lens/`, Gradio, ni Space HF.

## Documentación coherente

Si un cambio modifica el stack, defaults, first-run, scripts o fixtures, **en el mismo trabajo** hay que actualizar `README.md`, `docs/agenda/`, `research/README.md`, comentarios de `.env.example` y el change OpenSpec activo (`proposal` / `design` / `specs`). No dejar docs del default anterior.

Ítems diferidos: [docs/agenda/](docs/agenda/).

## Licencia del vendor

RAGFlow `docker/` se redistribuye bajo Apache-2.0. LedgerLens no modifica esos archivos.
