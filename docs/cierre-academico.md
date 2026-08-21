# Cierre académico (escritorio)

Checklist para la PC ≥16 GB (ideal 32 GB) **después** de merge. La notebook (~7 GB) ya cubre `./scripts/check.sh` sin Docker y sin Paddle.

Corpus cerrado: [`docs/archivos_muestra/`](archivos_muestra/) (10 PDF). Identidad = kernel (`identity_key` → claim). El chat no define cifras.

Pruebas: cuatro capas en [testing.md](testing.md) (archivos / identidad / inject mock / RAG vivo). Este archivo es el runbook de la **capa 4**. Un dump con `"skipped": true` no cuenta como piloto corrido.

## Requisitos del stack (capa 4)

| Requirement | Value |
|-----------|--------|
| Architecture | **x86_64** (not ARM64) |
| RAM | **≥ 16 GB** (32 GB recommended) |
| Disk | ≥ 50 GB |
| Docker | ≥ 24.0.0, Compose ≥ v2.26.1 |
| Kernel | `vm.max_map_count` ≥ 262144 |

RAGFlow does not read `.env` keys on its own. Configure Groq and Voyage under Model providers. Ollama from the container: `http://host.docker.internal:11434` (never `127.0.0.1`).

| Component | Default | Fallback |
|-------|---------|----------|
| UI + RAG | RAGFlow v0.26.4 :80 | — |
| Document engine | Infinity | not Elasticsearch |
| PDF parser | MinerU `pipeline` | Naive; DeepDoc; PaddleOCR (profile) |
| Chat | Groq `llama-3.3-70b-versatile` | Ollama `qwen2.5:1.5b` |
| Embeddings | Voyage `voyage-finance-2` | Gemini `gemini-embedding-001` |

First run: local sign-up; Model providers Groq + Voyage (+ MinerU via `MINERU_APISERVER`); knowledge base **`demo_4`** (Spanish, KG/RAPTOR off, page size **128**, parse one file at a time — [mineru-pipeline.md](agenda/mineru-pipeline.md)); assistant **`chat_demo_4`**, Show Quote on, threshold **0.3**. Then `python scripts/push_claims.py` and a **new** chat. Pilot knobs (rerank off): similarity threshold `0.3`, vector weight `0.3`.

## En la notebook (ya)

```bash
./scripts/check.sh
python scripts/idp_ask.py "¿Cuál es el resultado neto del período 1T26?"
python scripts/review_pack.py
python scripts/informe.py
```

`outputs/` está gitignored. Veredictos: copiá [`examples/review_verdicts.example.json`](../examples/review_verdicts.example.json) a `outputs/review_verdicts.json` si querés `reject`/`flag`. Sin archivo = todo `accept`.

## En el escritorio (≥16 GB)

1. `./scripts/check.sh` y `./scripts/up.sh`.
2. `python scripts/preprocess_probe.py` — orientación de tapa (`PP-LCNet_x1_0_doc_ori`). Sin Paddle: sale 0 y `no_paddle`. **No** es OCR de identidad; MinerU sigue siendo el parse.
3. Dataset `demo_4`, parser MinerU, knobs híbridos: Similarity threshold `0.3`, Vector similarity weight `0.3` (keyword 0.7). KG / RAPTOR / Auto-keyword off. Rerank `rerank-2.5-lite` opcional.
4. `python scripts/push_claims.py` y **chat nuevo**.
5. Cinco trampas a mano: neto 1T26 `21262335` (no controlante); controlante `21259769`; YPF empty; EBITDA deck `72128`; Show Quote al PDF del EEFF.
6. `python scripts/retrieval_bench.py` — tres brazos (weight 0 / 1 / 0.3), rerank off. Dump `outputs/retrieval_run.json`. Pegar Recall@5 / @10 / MRR en el README.
7. `python scripts/rag_eval.py` — 10 preguntas de chat **después** de `push_claims`. Dump `outputs/rag_chat_run.json`.

### Estado del run (escritorio)

Corrido: `push_claims`, trampas (neto/controlante/YPF/Show Quote OK; EBITDA deck abstain), `preprocess_probe` → `no_paddle`, bench + `rag_eval`. README actualizado con métricas reales. Retrieval keyword/vector/hybrid: Recall@5/10 **0.25**, MRR **0.125** (n=20). Chat: retrieval **0.7** / answer **0.6** / citation **0.7** / abstention **0.7** (n=10).

Rerank `rerank-2.5-lite` queda apagado durante el piloto de tres brazos. UVDoc fuera. Transcripción y memorias siguen sin extraer P&L.
