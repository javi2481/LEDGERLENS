# Cierre académico (escritorio)

Checklist para la PC ≥16 GB (ideal 32 GB) **después** de merge. La notebook (~7 GB) ya cubre `./scripts/check.sh` sin Docker y sin Paddle.

Corpus cerrado: [`docs/archivos_muestra/`](archivos_muestra/) (10 PDF). Identidad = kernel (`identity_key` → claim). El chat no define cifras.

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
6. Retrieval test: una pregunta de identidad (debe citar el claim inyectado) y una narrativa (keyword+vector, no cifra inventada).

UVDoc fuera. Transcripción y memorias siguen sin extraer P&L.
