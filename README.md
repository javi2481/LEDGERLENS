# LedgerLens

IDP **multi-dominio**: receta → extract → claims → lookup. Finanzas (EEFF BYMA) es el primer plugin. El chat RAGFlow es un **demo de portfolio**, no la fuente de verdad de identidad.

## Dos rieles

| Riel | Qué es | Cómo se prueba |
|------|--------|----------------|
| **Kernel IDP** (producto) | `schemas/` + `evals/` + `scripts/idp_ask.py` | `./scripts/check.sh` (pytest; sin Docker) |
| **Demo RAG** (portfolio) | Compose + MinerU + overlay Graph | PC ≥16 GB, `./scripts/up.sh`, UI `demo_4` |

SDD del producto (shipped): [`ledgerlens-idp-kernel`](openspec/changes/ledgerlens-idp-kernel/) y [`ledgerlens-finance-pnl-claims`](openspec/changes/ledgerlens-finance-pnl-claims/). Siguiente slice: [`docs/plan-siguiente-idp.md`](docs/plan-siguiente-idp.md). El change [`ledger-lens-ragflow`](openspec/changes/ledger-lens-ragflow/) está **congelado** como pin del demo.

## Oro (no fusionar)

Las cifras coinciden; los archivos no. Mezclarlos vuelve a confundir fila vecina con chunk.

| Rol | Archivo |
|-----|---------|
| Contrato IDP | `recipes/financial_statement.json` + [`evals/identity_v1.json`](evals/identity_v1.json) + [`evals/identity_v2.json`](evals/identity_v2.json) |
| Overlay del chat | [`docs/hechos_eeff.json`](docs/hechos_eeff.json) (lo inyecta `push_hechos.py`) |

Corpus: `docs/archivos_muestra/` (comunicados, EEFF, presentaciones, memoria).

## Quick path (kernel, cualquier PC)

1. `uv venv && uv pip install -r requirements-dev.txt`
2. `./scripts/check.sh`
3. `python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"` → `21262335` (consolidado, página 4)

Trampas: sin decir controlante → consolidado neto (`21262335` / `81956525`). Controlante explícito → la otra cifra. Bruto ≠ operativo ≠ neto. Impuesto 1T26 → `-14950948`. No controlante → `2566`, no el controlante. YPF / memoria / comunicado → abstain. Los 10 casos `route: narrative` se saltan (capa 3). Detalle: [docs/testing.md](docs/testing.md).

## Riel demo (PC ≥16 GB, x86_64)

Stack: **RAGFlow** v0.26.4 + Infinity. Parser **MinerU** `pipeline`. Chat **Groq** `llama-3.3-70b-versatile` + Ollama fallback. Embed **Voyage**. **PaddleOCR** apagado por defecto.

1. Docker ≥24, **Compose v2**, usuario en `docker`, `vm.max_map_count` ≥ 262144.
2. Copiar `.env.example` → `.env`. Pegar keys (**.env no está en git**).
3. `./scripts/check.sh` y `./scripts/up.sh`. UI: <http://localhost>
4. Groq + Voyage, dataset **`demo_4`**, parser **MinerU**, Empty response + Show Quote. Runbook: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).

Compose + E2E viven en la PC Windows 32 GB. En ~7 GB: solo el kernel. Diferidos del **demo**: [docs/agenda/](docs/agenda/).

### Stack del demo

| Pieza | Default | Fallback / opcional |
|-------|---------|---------------------|
| UI + RAG | RAGFlow **v0.26.4** puerto 80 | — |
| Motor docs | **Infinity** | no Elasticsearch |
| Parser PDF | **MinerU** `pipeline` (`MINERU_APISERVER=http://mineru-api:8000`) | Naive; DeepDoc (escaneos); PaddleOCR (profile) |
| Chat | Groq `llama-3.3-70b-versatile` | Ollama `qwen2.5:1.5b` |
| Embeddings | Voyage `voyage-finance-2` (nativo v0.26.4) | Gemini `gemini-embedding-001` |
| Empty response | `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.` | no dejar en blanco |

RAGFlow **no** lee las API keys solo: pegá Groq y Voyage en Model providers. Ollama, si lo usás: `http://host.docker.internal:11434` (**nunca** `127.0.0.1` desde el contenedor). MinerU hybrid pide GPU; no entra. OpenRouter Nano `:free` no es el default.

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
2. **Model providers**
   - **Groq:** `llama-3.3-70b-versatile` (chat default). Pegá `GROQ_API_KEY` en la factory.
   - Voyage: `voyage-finance-2` (embed) y `rerank-2.5-lite`.
   - MinerU: auto-provision con `MINERU_APISERVER` en `.env`, o agregarlo a mano.
   - Ollama (fallback): `http://host.docker.internal:11434`, modelo `qwen2.5:1.5b`. No uses OpenRouter Nano `:free`.
3. Knowledge base **`demo_4`**: **Configuración primero** (PDF parser = **MinerU**; español; Knowledge graph y RAPTOR off). **Después** subir `docs/archivos_muestra/*.pdf`. En cada file, **Tamaño de la tarea por página = 128**. **Por último** Parse, de a uno. Si MinerU está caído, el ingest debe fallar visible (no texto inventado). Detalle: [docs/agenda/mineru-pipeline.md](docs/agenda/mineru-pipeline.md).
4. Chat en español: asistente **`chat_demo_4`**, KB tildada, **Show Quote** on, umbral **0.3**, Empty response no vacío. Graph: `python scripts/push_hechos.py` y un **chat nuevo**.

Ollama en el host, si lo usás:

```bash
export OLLAMA_HOST=0.0.0.0
ollama pull qwen2.5:1.5b
```

### Overlay Graph (solo demo)

No es el kernel IDP. **No** va en `up.sh` ni Compose. **No** re-parsea MinerU. Gold de este riel: [`docs/hechos_eeff.json`](docs/hechos_eeff.json).

1. Extraer fichas: `python scripts/run_docling_graph_eeff.py` (un filing, `--preset`, o `--all`).
2. Inyectar: `python scripts/push_hechos.py` (stack arriba + token RAGFlow). Un chat ya abierto no toma el prompt nuevo.

Detalle: [docs/agenda/docling-graph.md](docs/agenda/docling-graph.md). `outputs/` está en gitignore.

### Opcional: Naive / DeepDoc / PaddleOCR

MinerU es el default para EEFF con tablas. Naive si el API no está. DeepDoc si no hay capa de texto. PaddleOCR: `COMPOSE_PROFILES=infinity,cpu,paddleocr`, descomentar vars en `.env`, factory `http://paddleocr:8080/layout-parsing`, `PP-StructureV3`, token vacío.

## Repo

| Path | Rol | Riel |
|------|-----|------|
| `schemas/` / `recipes/` / `evals/` | Kernel IDP | producto |
| `scripts/idp_ask.py` | Lookup sin RAGFlow | producto |
| `openspec/changes/ledgerlens-finance-pnl-claims/` | SDD P&L shipped | producto |
| `openspec/changes/ledgerlens-idp-kernel/` | SDD kernel shipped | producto |
| `vendor/ragflow-docker/` | Pin v0.26.4. No editar. [vendor/PIN.md](vendor/PIN.md) | demo |
| `docker-compose.overlay.yml` / `docker/mineru/` | Sidecar MinerU | demo |
| `scripts/up.sh` | Arranque Compose | demo |
| `scripts/push_hechos.py` / `docs/hechos_eeff.json` | Overlay Graph | demo |
| `openspec/changes/ledger-lens-ragflow/` | SDD congelado (pin) | demo |
| `scripts/check.sh` | Contratos + pytest | ambos |
| `docs/archivos_muestra/` | PDFs BYMA | ambos |
| `docs/agenda/` | Diferidos del **demo** (vLLM, branding, gancho Graph) | demo |
| `research/` | Dumps Parallel | — |

No hay `app.py`, `ledger_lens/`, Gradio, ni Space HF.

## Documentación coherente

Producto: actualizar `README.md` y el change OpenSpec **abierto** en el mismo trabajo (hoy no hay change activo; siguiente: [docs/plan-siguiente-idp.md](docs/plan-siguiente-idp.md)). Demo: `docs/agenda/`, `research/README.md`, `.env.example` y el change congelado solo si cambia el pin.

Ítems diferidos del demo: [docs/agenda/](docs/agenda/).

## Licencia del vendor

RAGFlow `docker/` se redistribuye bajo Apache-2.0. LedgerLens no modifica esos archivos.
