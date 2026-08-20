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
grep -q 'mineru-api:' docker-compose.overlay.yml || fail "overlay must define mineru-api sidecar"
grep -q '^MINERU_APISERVER=http://mineru-api:8000' .env.example || fail ".env.example must set MINERU_APISERVER to Compose DNS"
grep -q '^MINERU_BACKEND=pipeline' .env.example || fail ".env.example must set MINERU_BACKEND=pipeline"
grep -q '^USE_DOCLING=false' .env.example || fail ".env.example must keep USE_DOCLING=false (MinerU is the parser)"
if grep -qE '^DOCLING_SERVER_URL=' .env.example; then
  fail ".env.example must not set DOCLING_SERVER_URL"
fi
[[ -f docker/mineru/Dockerfile ]] || fail "missing docker/mineru/Dockerfile"
[[ -f scripts/up.sh ]] || fail "missing scripts/up.sh"
bash -n scripts/up.sh || fail "scripts/up.sh failed bash -n"
[[ -f .env.example ]] || fail "missing .env.example"
grep -q '^DOC_ENGINE=infinity' .env.example || fail ".env.example must set DOC_ENGINE=infinity"
grep -qE '^# GROQ_API_KEY=' .env.example || fail ".env.example must keep GROQ_API_KEY commented"
if grep -qE '^GROQ_API_KEY=gsk_' .env.example; then
  fail ".env.example must not contain a real Groq key"
fi
grep -qE '^# GEMINI_API_KEY=' .env.example || fail ".env.example must keep GEMINI_API_KEY commented (unused factory)"
if grep -qE '^GEMINI_API_KEY=AIza' .env.example; then
  fail ".env.example must not contain a real Gemini key"
fi
if grep -qE '^OPENROUTER_API_KEY=' .env.example; then
  fail ".env.example must not set OPENROUTER_API_KEY (OpenRouter is not the default chat)"
fi
[[ ! -e app.py ]] || fail "forbidden app.py"
[[ ! -d ledger_lens ]] || fail "forbidden ledger_lens/"
git check-ignore -q .env || fail ".env must be gitignored"
[[ -f recipes/financial_statement.json ]] || fail "missing recipes/financial_statement.json"
[[ -f schemas/financial_statement.py ]] || fail "missing schemas/financial_statement.py"
[[ -f schemas/catalog.py ]] || fail "missing schemas/catalog.py"
[[ -f schemas/claim.py ]] || fail "missing schemas/claim.py"
[[ -f evals/identity_v1.json ]] || fail "missing evals/identity_v1.json"
[[ -f evals/identity_v2.json ]] || fail "missing evals/identity_v2.json"
[[ -f evals/press_v1.json ]] || fail "missing evals/press_v1.json"
[[ -f schemas/finance_lines.py ]] || fail "missing schemas/finance_lines.py"
[[ -f schemas/press_release.py ]] || fail "missing schemas/press_release.py"
[[ -f schemas/store.py ]] || fail "missing schemas/store.py"
[[ -f scripts/idp_ask.py ]] || fail "missing scripts/idp_ask.py"
if [[ -e recipes/UNKNOWN.json ]] || [[ -e recipes/unknown.json ]]; then
  fail "UNKNOWN is a classifier class, not a recipe file"
fi
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
    skip "compose/E2E: RAM < 16 GiB — see docs/agenda/descartado.md"
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
  info "ollama on PATH (optional last fallback; default chat is Groq llama-3.3-70b-versatile)"
else
  skip "ollama not on PATH (ok — default chat is Groq)"
fi

pass "chat default is Groq llama-3.3-70b-versatile (no OpenRouter default)"

# --- IDP kernel pytest (capa 1-2; no RAGFlow) ---
PY=python3
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
fi
if ! "$PY" -c "import pytest, pydantic" >/dev/null 2>&1; then
  fail "pytest+pydantic required — uv venv && uv pip install -r requirements-dev.txt"
fi
"$PY" -m pytest tests/ -q || fail "pytest tests/"
pass "pytest IDP capa 1-2"

echo
echo "Done. Compose/E2E remains on a ≥16 GB host."
