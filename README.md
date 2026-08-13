# LedgerLens

Preguntas en español sobre PDFs financieros sintéticos, con citas a la fuente. Si no hay evidencia, el asistente responde vacío (no inventa). El frontend y el RAG son **RAGFlow** self-host; el parser es **PaddleOCR** self-host; el LLM corre en **Ollama** en el host.

Esto es un demo de portfolio. Los PDFs de `examples/synthetic/` son ficticios. **No** son filings de BYMA ni de emisores reales.

## Requisitos

| Requisito | Valor |
|-----------|--------|
| Arquitectura | **x86_64** (las imágenes oficiales de RAGFlow no cubren ARM64) |
| RAM | **≥ 16 GB** (RAGFlow + PaddleOCR CPU + Ollama) |
| Disco | ≥ 50 GB |
| Docker | ≥ 24.0.0 |
| Compose | ≥ v2.26.1 |
| Kernel | `vm.max_map_count` ≥ 262144 |
| Ollama | en el host, escuchando en `0.0.0.0:11434` |

Esta máquina de desarrollo puede no cumplir RAM/Docker: en ese caso el stack no se levanta aquí; el arranque real es en un host ≥16 GB x86 con Docker.

### `vm.max_map_count`

Comprobar (solo lectura):

```bash
cat /proc/sys/vm/max_map_count
```

Si es menor que 262144, como root (no lo hace `scripts/up.sh`):

```bash
sudo sysctl -w vm.max_map_count=262144
```

Para persistir, agregar `vm.max_map_count=262144` en `/etc/sysctl.conf`.

### Ollama en el host

```bash
export OLLAMA_HOST=0.0.0.0
# reiniciar el servicio Ollama para que el bind aplique
ollama pull qwen2.5:1.5b
ollama pull bge-m3
```

Desde el contenedor RAGFlow la URL es `http://host.docker.internal:11434`. **Nunca** uses `http://127.0.0.1:11434` dentro de RAGFlow: eso apunta al propio contenedor.

## Arranque

```bash
cp .env.example .env
./scripts/up.sh
```

El script:

1. Falla si `vm.max_map_count` < 262144 y **no** declara el demo listo.
2. Copia `.env` a `vendor/ragflow-docker/.env` (el compose oficial lee `env_file: .env` al lado de sus YAML).
3. Levanta RAGFlow **v0.26.4** (Infinity + CPU) más el overlay de PaddleOCR.
4. Intenta `ollama pull qwen2.5:1.5b` y `bge-m3`.

UI: [http://localhost](http://localhost) (puerto 80).

PaddleOCR no se publica en el host. RAGFlow lo llama por DNS de Compose: `http://paddleocr:8080/layout-parsing` con algoritmo `PP-StructureV3`. No hace falta token de AI Studio.

Parar y borrar volúmenes:

```bash
docker compose --env-file .env \
  -f vendor/ragflow-docker/docker-compose.yml \
  -f docker-compose.overlay.yml down -v
```

## Primera vez en la UI (español)

1. Crear cuenta (registro local de RAGFlow).
2. **Model providers**
   - Añadir **Ollama**:
     - Chat: `qwen2.5:1.5b` — base URL `http://host.docker.internal:11434`
     - Embedding: `bge-m3` — misma base URL
   - Añadir **PaddleOCR** (factory OCR):
     - API URL: `http://paddleocr:8080/layout-parsing`
     - Algorithm: `PP-StructureV3`
     - Access token: vacío
3. **Knowledge base** llamado `LedgerLens`
   - Parser PDF: **PaddleOCR**
   - Subir los cuatro PDFs de `examples/synthetic/`
   - Esperar a que el parseo termine (si el parser está caído, el ingest debe fallar a la vista; no debe aparecer texto inventado)
4. **Chat assistant** en español
   - Knowledge base: `LedgerLens`
   - **Show Quote**: activado
   - Umbral de similitud: alto (p. ej. 0.4 o el máximo que aún recupere los hechos sintéticos)
   - **Empty response** (obligatorio, no dejar en blanco):

     `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.`

   - Prompt de sistema (ejemplo):

     `Responde solo en español. Cita los fragmentos recuperados. Si no hay evidencia, usa la respuesta vacía configurada. No inventes cifras ni hechos.`

## Checklist E2E manual

Con el stack healthy (`ragflow-cpu` en :80, servicio `paddleocr` up, `ollama list` muestra `qwen2.5:1.5b` y `bge-m3`):

1. **Ingest** — subir los cuatro PDFs sintéticos (hechos, estados, memoria, operativo) con parser PaddleOCR. El parseo debe usar `http://paddleocr:8080/layout-parsing`, no `localhost`.
2. **Pregunta con evidencia** — p. ej. *¿Por cuánto vendió Acme Norte la planta Rosario?* Debe responder en español y mostrar **Show Quote** (ARS 1.250 millones, 12 de marzo de 2025).
3. **Pregunta sin evidencia** — p. ej. *¿Cuál fue el precio de cierre de YPF en BYMA el 3 de enero?* Debe devolver exactamente el Empty response en español, **sin** inventar cifras ni citas.
4. **Segundo documento** — p. ej. *¿Cuántos pallets despachó Acme Norte en el Q1 2025?* Debe citar el informe operativo (18.400).
5. **Parser caído** — `docker compose ... stop paddleocr` y reintentar un ingest: debe fallar de forma visible, sin fabricar texto.

## Qué incluye el repo

- `vendor/ragflow-docker/` — pin oficial `docker/` de RAGFlow **v0.26.4** (Apache-2.0). No editar. Ver `vendor/PIN.md`.
- `docker-compose.overlay.yml` — servicio `paddleocr` en la red `ragflow`, sin publicar `:8080`.
- `docker/paddleocr/Dockerfile` — PaddleX `PP-StructureV3` CPU, `POST /layout-parsing`.
- `.env.example` — `DOC_ENGINE=infinity`, imagen `infiniflow/ragflow:v0.26.4`, URL Compose-DNS de PaddleOCR.
- `scripts/up.sh` — sysctl de solo lectura, compose, pulls de Ollama.
- `examples/synthetic/` — cuatro PDFs en español, ficticios.

No hay `app.py`, paquete `ledger_lens/`, Gradio, ni Space de Hugging Face.

## Licencia del vendor

RAGFlow `docker/` se redistribuye bajo Apache-2.0. LedgerLens no modifica esos archivos.
