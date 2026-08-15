#!/usr/bin/env bash
# Host-level checks that run without RAGFlow. Skip compose (needs ≥16 GB + Docker Compose).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
skip() { echo "SKIP: $*"; }
info() { echo "INFO: $*"; }

echo "== LedgerLens check (no RAGFlow runtime) =="

# --- file contracts ---
[[ -f vendor/PIN.md ]] || fail "missing vendor/PIN.md"
grep -q 'v0.26.4' vendor/PIN.md || fail "vendor/PIN.md must pin v0.26.4"
[[ -f vendor/ragflow-docker/docker-compose.yml ]] || fail "missing vendor compose"
[[ -f docker-compose.overlay.yml ]] || fail "missing docker-compose.overlay.yml"
grep -q 'profiles:' docker-compose.overlay.yml || fail "overlay must gate paddleocr on a profile"
grep -q 'docling-serve:' docker-compose.overlay.yml || fail "overlay must define docling-serve sidecar"
grep -q '^DOCLING_SERVER_URL=http://docling-serve:5001' .env.example || fail ".env.example must set DOCLING_SERVER_URL to Compose DNS"
grep -q '^USE_DOCLING=false' .env.example || fail ".env.example must keep USE_DOCLING=false (sidecar, not in-process)"
[[ -f scripts/up.sh ]] || fail "missing scripts/up.sh"
bash -n scripts/up.sh || fail "scripts/up.sh failed bash -n"
[[ -f .env.example ]] || fail "missing .env.example"
grep -q '^DOC_ENGINE=infinity' .env.example || fail ".env.example must set DOC_ENGINE=infinity"
grep -qE '^# OPENROUTER_API_KEY=' .env.example || fail ".env.example must keep OPENROUTER_API_KEY commented"
if grep -qE '^OPENROUTER_API_KEY=sk-' .env.example; then
  fail ".env.example must not contain a real OpenRouter key"
fi
[[ ! -e app.py ]] || fail "forbidden app.py"
[[ ! -d ledger_lens ]] || fail "forbidden ledger_lens/"
git check-ignore -q .env || fail ".env must be gitignored"
pass "file contracts"

# --- sample PDFs (BYMA filings for the live demo) ---
command -v pdftotext >/dev/null 2>&1 || fail "pdftotext required (poppler-utils) for fixture checks"
mapfile -t pdfs < <(ls docs/archivos_muestra/*.pdf 2>/dev/null || true)
[[ ${#pdfs[@]} -ge 6 ]] || fail "expected ≥6 PDFs in docs/archivos_muestra/, got ${#pdfs[@]}"

expect_in() {
  local file="$1" needle="$2"
  pdftotext -layout "$file" - | grep -Fq "$needle" || fail "$file missing: $needle"
}

comunicado=""
for f in docs/archivos_muestra/*.pdf; do
  case "$f" in
    *Comunicado*1T26*) comunicado="$f" ;;
  esac
done
[[ -n "$comunicado" ]] || fail "missing BYMA comunicado 1T26 in docs/archivos_muestra/"
expect_in "$comunicado" "BYMA"
pass "BYMA sample PDFs"

# --- host probe (informational; does not fail) ---
arch="$(uname -m)"
info "arch=$arch"
[[ "$arch" == "x86_64" ]] || skip "RAGFlow images are x86_64; this host is $arch"

if [[ -r /proc/meminfo ]]; then
  mem_kb="$(awk '/MemTotal:/ {print $2}' /proc/meminfo)"
  mem_gb=$((mem_kb / 1024 / 1024))
  info "MemTotal≈${mem_gb} GiB (RAGFlow wants ≥16)"
  if (( mem_gb < 16 )); then
    skip "compose/E2E: RAM < 16 GiB — see docs/agenda/e2e-16gb.md"
  fi
fi

if [[ -r /proc/sys/vm/max_map_count ]]; then
  map_count="$(tr -d '[:space:]' < /proc/sys/vm/max_map_count)"
  info "vm.max_map_count=$map_count (need ≥262144)"
else
  skip "cannot read vm.max_map_count"
fi

if command -v docker >/dev/null 2>&1; then
  info "docker CLI $(docker --version 2>/dev/null | head -1)"
  if docker info >/dev/null 2>&1; then
    info "docker daemon reachable"
  else
    skip "docker daemon not usable (group docker / daemon down)"
  fi
  if docker compose version >/dev/null 2>&1; then
    info "$(docker compose version)"
  else
    skip "Docker Compose v2 plugin missing (scripts/up.sh needs it)"
  fi
else
  skip "docker CLI not installed"
fi

if command -v ollama >/dev/null 2>&1; then
  info "ollama on PATH (fallback chat; default is OpenRouter)"
else
  skip "ollama not on PATH (ok — OpenRouter is default chat)"
fi

# --- OpenRouter smoke (optional) ---
key=""
if [[ -f .env ]]; then
  key="$(python3 - <<'PY'
from pathlib import Path
p = Path(".env")
for line in p.read_text().splitlines():
    if line.startswith("OPENROUTER_API_KEY="):
        print(line.split("=", 1)[1].strip().strip("\"'"))
PY
)"
fi
if [[ -z "$key" ]]; then
  skip "OpenRouter smoke: no OPENROUTER_API_KEY in .env"
else
  code="$(curl -sS -o /tmp/ledgerlens-or-models.json -w '%{http_code}' \
    --max-time 30 \
    -H "Authorization: Bearer $key" \
    https://openrouter.ai/api/v1/models || true)"
  if [[ "$code" == "200" ]]; then
    pass "OpenRouter models endpoint (HTTP 200)"
  else
    fail "OpenRouter models endpoint HTTP ${code:-none} (key present, request failed)"
  fi
  embed_code="$(curl -sS -o /tmp/ledgerlens-or-embed.json -w '%{http_code}' \
    --max-time 60 \
    -H "Authorization: Bearer $key" \
    -H "Content-Type: application/json" \
    -d '{"model":"nvidia/nemotron-3-embed-1b:free","input":"Acme Norte planta Rosario"}' \
    https://openrouter.ai/api/v1/embeddings || true)"
  if [[ "$embed_code" == "200" ]]; then
    pass "OpenRouter embed nvidia/nemotron-3-embed-1b:free"
  else
    fail "OpenRouter embed HTTP ${embed_code:-none}"
  fi
fi

echo
echo "Done. Compose/E2E remains on a ≥16 GB host."
