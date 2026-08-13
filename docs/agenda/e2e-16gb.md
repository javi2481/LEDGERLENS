# E2E en host ≥16 GB (agenda)

Esta PC **tiene Docker instalado** (`docker.io` 29.1.3, daemon `active`). No alcanza para RAGFlow: ~7,4 GB RAM, el usuario `javier` no está en el grupo `docker`, y no hay plugin Compose v2 (`docker compose`).

## Quick path (cuando haya ≥16 GB)

1. `sudo usermod -aG docker $USER` y re-login. Instalar Compose v2 (`docker-compose-v2` / plugin). RAM ≥ 16 GB.
2. `cp .env.example .env` y `OPENROUTER_API_KEY` (nunca commitear).
3. `./scripts/up.sh` → UI en :80.
4. Primera vez en la UI (README): OpenRouter chat+embed; parser **Naive**; Ollama solo si OpenRouter cae.
5. Checklist E2E del README (ingest Naive, citas, empty response).

## Details

| Chequeo en esta PC (2026-08-13) | Valor |
|---------------------------------|--------|
| RAM | 7,4 GiB (hace falta ≥ 16) |
| Arch | x86_64 (ok) |
| `vm.max_map_count` | 1048576 (ok) |
| Docker | `docker.io` 29.1.3; daemon **active**; socket `root:docker` |
| Permiso | `javier` **no** está en grupo `docker` → `permission denied` en el socket |
| Compose v2 | no instalado (`docker compose` no existe; `/usr/bin/compose` es mailcap) |
| Ollama | binario presente; lista vacía |
| Disco | holgado (≥ 50 GB libres) |

## Checklist

- [x] `./scripts/check.sh` verde en esta PC (contratos + PDFs + OpenRouter smoke)
- [ ] Usuario en grupo `docker` + Compose v2
- [ ] Compose healthy en host ≥16 GB
- [ ] Ingest de los cuatro PDFs con **Naive**
- [ ] Pregunta Rosario → cita ARS 1.250 millones
- [ ] Pregunta YPF/BYMA → empty response
- [ ] Pregunta pallets → 18.400

## Next step

No forzar `./scripts/up.sh` aquí: OOM. El CLI de Docker solo no alcanza.
