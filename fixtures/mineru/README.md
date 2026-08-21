# MinerU parse artifacts

Texto durable del parse MinerU (un archivo por PDF de `docs/archivos_muestra/`). El kernel clasifica y extrae **solo** desde acá.

## Quick path

1. Con `demo_4` ya parseado: `python scripts/export_mineru.py`
2. Sin RAGFlow (host de docs): `python scripts/export_mineru.py --bootstrap-layout`
3. `./scripts/check.sh`

`--bootstrap-layout` materializa el mismo formato `<!-- page: N -->` con poppler. El kernel **no** llama `pdftotext`. En la PC del demo, re-exportar desde chunks MinerU pisa estos archivos.

No recortar memorias: un parse completo.
