# Vendor pin

| Field | Value |
|-------|--------|
| Package | Official RAGFlow `docker/` assets |
| Upstream | https://github.com/infiniflow/ragflow |
| Tag | **v0.26.4** |
| Source tarball | https://github.com/infiniflow/ragflow/archive/refs/tags/v0.26.4.tar.gz |
| License | Apache-2.0 (copy in `vendor/ragflow-docker/LICENSE`) |

Do **not** edit files under `vendor/ragflow-docker/` except to refresh the pin. Overlay, env, and PaddleOCR live in this repo outside `vendor/`.

`vendor/ragflow-docker/.env` is generated at runtime by `scripts/up.sh` (copy of the repo-root `.env`) and is gitignored.
