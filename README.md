# LedgerLens

Demo de portfolio: preguntas en **español** sobre PDFs financieros de **BYMA**, con citas. Si no hay evidencia, responde vacío (no inventa).

Stack: **RAGFlow** v0.26.4 self-host (UI + RAG) + Infinity. Parser **Docling** clásico (sidecar CPU, no VLM). Chat **OpenRouter**. Embed **Voyage**. **Ollama** es fallback. **PaddleOCR** no arranca por defecto.

Corpus: `docs/archivos_muestra/` (comunicados, EEFF, presentaciones, memoria).

## Quick path (PC ≥16 GB, x86_64)

1. Instalar Docker ≥24 y **Compose v2** (`docker compose version`). Tu usuario en el grupo `docker`. `vm.max_map_count` ≥ 262144.
2. Clonar `https://github.com/javi2481/LEDGERLENS`. Copiar `.env.example` → `.env`. Pegar keys (**.env no está en git**).
3. `./scripts/check.sh` y después `./scripts/up.sh`. UI: <http://localhost>
4. En la UI: OpenRouter chat + Voyage embed, dataset `demo_1`, parser **Docling**, Empty response + Show Quote (abajo).

En una PC de ~7 GB: solo `./scripts/check.sh`. Compose + E2E: esta PC Windows 32 GB. Diferidos: [docs/agenda/](docs/agenda/).

## Stack (fuente de verdad del demo)

| Pieza | Default | Fallback / opcional |
|-------|---------|---------------------|
| UI + RAG | RAGFlow **v0.26.4** puerto 80 | — |
| Motor docs | **Infinity** | no Elasticsearch |
| Parser PDF | **Docling** clásico (`DOCLING_SERVER_URL=http://docling-serve:5001`) | Naive; DeepDoc (escaneos); PaddleOCR (profile) |
| Chat | OpenRouter `nvidia/nemotron-3-nano-30b-a3b:free` | Ollama `qwen2.5:1.5b` en `http://host.docker.internal:11434` |
| Embeddings | Voyage `voyage-finance-2` (nativo v0.26.4) | Gemini `gemini-embedding-001` |
| Empty response | `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.` | no dejar en blanco |

RAGFlow **no** lee `OPENROUTER_API_KEY` solo: hay que pegarla en Model providers. Nunca `127.0.0.1` para Ollama desde el contenedor. `USE_DOCLING=false`: Docling corre en el sidecar, no in-process. Granite-Docling VLM no entra en este demo.

## Requisitos

| Requisito | Valor |
|-----------|--------|
| Arquitectura | **x86_64** (imágenes oficiales, no ARM64) |
| RAM | **≥ 16 GB** (32 GB recomendado: RAGFlow + Docling Serve CPU) |
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

`up.sh` falla si `vm.max_map_count` es bajo; copia `.env` a `vendor/ragflow-docker/.env`; levanta Infinity+CPU+Docling Serve; PaddleOCR queda apagado; pull de Ollama solo si está instalado.

Parar:

```bash
docker compose --env-file .env \
  -f vendor/ragflow-docker/docker-compose.yml \
  -f docker-compose.overlay.yml down -v
```

## Primera vez en la UI

1. Registro local.
2. **Model providers**
   - OpenRouter: misma key que `.env`. Chat `nvidia/nemotron-3-nano-30b-a3b:free`.
   - Voyage: `voyage-finance-2` (embed). Defaults en System Model Settings.
   - Ollama (fallback): `qwen2.5:1.5b`, URL `http://host.docker.internal:11434`.
3. Knowledge base: **Configuración primero** (Reconocimiento de disposición = **Docling**; Knowledge graph y RAPTOR off). **Después** subir `docs/archivos_muestra/*.pdf`. **Por último** Parse, de a uno. Si Docling Serve está caído, el ingest debe fallar visible (no texto inventado). Cambiar Configuración no pisa archivos ya subidos.
4. Chat en español: KB tildada, **Show Quote** on, umbral alto (p. ej. 0.4), Empty response no vacío (copy de la tabla de stack). Prompt: *Responde solo en español. Cita los fragmentos. Si no hay evidencia, usa la respuesta vacía. No inventes cifras.*

Ollama en el host, si lo usás:

```bash
export OLLAMA_HOST=0.0.0.0
ollama pull qwen2.5:1.5b
```

## Checklist E2E

Con `ragflow-cpu` en :80, `docling-serve` healthy y Voyage configurado:

1. Ingest Docling de los PDFs de `docs/archivos_muestra/` (empezar por comunicados; EEFF y Memoria al final).
2. *¿Cuál es el RESULTADO NETO DEL PERÍODO consolidado del EEFF?* → español + Show Quote (número del PDF, no inventado).
3. *¿Cuál fue el precio de cierre de YPF en BYMA el 3 de enero?* → Empty response, sin inventar.

Un clone de GitHub **no** trae chunks: Infinity/MySQL/MinIO viven en volúmenes Docker. Quien pruebe el repo parsea en su máquina. El parseo previo es de **esta instancia** (demo LinkedIn / screenshots).

## Opcional: Naive / DeepDoc / PaddleOCR

Docling es el default para EEFF con tablas. Naive si Serve no está. DeepDoc si no hay capa de texto. PaddleOCR: `COMPOSE_PROFILES=infinity,cpu,paddleocr`, descomentar vars en `.env`, factory `http://paddleocr:8080/layout-parsing`, `PP-StructureV3`, token vacío.

## Repo

| Path | Rol |
|------|-----|
| `vendor/ragflow-docker/` | Pin oficial v0.26.4. No editar. [vendor/PIN.md](vendor/PIN.md) |
| `docker-compose.overlay.yml` | Docling Serve CPU + PaddleOCR opcional, sin `:8080` |
| `.env.example` | Infinity + pin; `DOCLING_SERVER_URL`; PaddleOCR comentado |
| `scripts/up.sh` / `scripts/check.sh` | Arranque / contratos+PDFs+OpenRouter |
| `docs/archivos_muestra/` | PDFs BYMA del demo |
| `docs/agenda/` | Diferidos (Graph, vLLM, branding, LinkedIn) |
| `research/` | Dumps Parallel |
| `openspec/changes/ledger-lens-ragflow/` | SDD activo (Gentle AI hybrid) |

No hay `app.py`, `ledger_lens/`, Gradio, ni Space HF. Ignorar `openspec/changes/ledger-lens-mvp/` (residuo Gradio).

## Documentación coherente

Si un cambio modifica el stack, defaults, first-run, scripts o fixtures, **en el mismo trabajo** hay que actualizar `README.md`, `docs/agenda/`, `research/README.md`, comentarios de `.env.example` y el change OpenSpec activo (`proposal` / `design` / `specs`). No dejar docs del default anterior.

Ítems diferidos: [docs/agenda/](docs/agenda/).

## Licencia del vendor

RAGFlow `docker/` se redistribuye bajo Apache-2.0. LedgerLens no modifica esos archivos.
