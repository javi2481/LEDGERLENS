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

# --- synthetic PDFs ---
command -v pdftotext >/dev/null 2>&1 || fail "pdftotext required (poppler-utils) for fixture checks"
mapfile -t pdfs < <(ls examples/synthetic/*.pdf 2>/dev/null || true)
[[ ${#pdfs[@]} -eq 4 ]] || fail "expected 4 PDFs in examples/synthetic/, got ${#pdfs[@]}"

expect_in() {
  local file="$1" needle="$2"
  pdftotext -layout "$file" - | grep -Fq "$needle" || fail "$file missing: $needle"
}

expect_in examples/synthetic/hechos-relevantes-acme-norte.pdf "No es un filing de BYMA"
expect_in examples/synthetic/hechos-relevantes-acme-norte.pdf "ARS 1.250 millones"
expect_in examples/synthetic/hechos-relevantes-acme-norte.pdf "12 de marzo de 2025"
expect_in examples/synthetic/informe-operativo-acme-norte-q1-2025.pdf "18.400"
expect_in examples/synthetic/estados-financieros-acme-norte-2024.pdf "ARS 4.800 millones"
expect_in examples/synthetic/memoria-acme-norte-2024.pdf "120 empleados"
pass "synthetic PDF fixtures"

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
echo "Done. Compose/E2E remains on a ≥16 GB host — docs/agenda/e2e-16gb.md"
