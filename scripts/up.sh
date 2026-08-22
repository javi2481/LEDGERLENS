#!/usr/bin/env bash
# Start Claimprint: official RAGFlow v0.26.4 (Infinity). UI parser default: MinerU (pipeline CPU).
# Chat demo is Mistral mistral-small-latest in the UI. Host Ollama is last fallback.
# Optional: COMPOSE_PROFILES=infinity,cpu,paddleocr to also start PaddleOCR.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MIN_MAP_COUNT=262144
VENDOR_COMPOSE="$ROOT/vendor/ragflow-docker/docker-compose.yml"
OVERLAY="$ROOT/docker-compose.overlay.yml"
ENV_FILE="$ROOT/.env"
ENV_EXAMPLE="$ROOT/.env.example"

fail() {
  echo "error: $*" >&2
  exit 1
}

if [[ ! -f "$VENDOR_COMPOSE" ]]; then
  fail "missing $VENDOR_COMPOSE (vendor pin v0.26.4)"
fi

if [[ ! -f "$ENV_FILE" ]]; then
  if [[ -f "$ENV_EXAMPLE" ]]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "created .env from .env.example"
  else
    fail "missing .env and .env.example"
  fi
fi

if ! command -v docker >/dev/null 2>&1; then
  fail "Docker is required (Docker ≥24, Compose ≥v2.26.1). Demo not ready."
fi

if ! docker compose version >/dev/null 2>&1; then
  fail "Docker Compose v2 is required. Demo not ready."
fi

if [[ ! -r /proc/sys/vm/max_map_count ]]; then
  fail "cannot read vm.max_map_count. Demo not ready."
fi

map_count="$(tr -d '[:space:]' < /proc/sys/vm/max_map_count)"
if [[ "$map_count" -lt "$MIN_MAP_COUNT" ]]; then
  echo "error: vm.max_map_count is $map_count (need ≥ $MIN_MAP_COUNT)." >&2
  echo "Set it as root (documented in README): sysctl -w vm.max_map_count=$MIN_MAP_COUNT" >&2
  echo "Demo not ready." >&2
  exit 1
fi

mkdir -p "$ROOT/vendor/ragflow-docker"
cp "$ENV_FILE" "$ROOT/vendor/ragflow-docker/.env"

echo "starting RAGFlow v0.26.4 (Infinity; MinerU parser; Mistral chat)..."
docker compose --env-file "$ENV_FILE" \
  -f "$VENDOR_COMPOSE" \
  -f "$OVERLAY" \
  up -d

echo
echo "RAGFlow UI: http://localhost (port 80)"
echo "PDF parser default for this demo: MinerU pipeline (sidecar :8000). Naive/DeepDoc if MinerU is down. PaddleOCR: profile paddleocr."
echo "Chat demo: Mistral mistral-small-latest (paste key in Model providers; thr 0.2 after push_claims)."
echo "Ollama last fallback: http://host.docker.internal:11434  (never 127.0.0.1)"
echo "Embeddings: Voyage voyage-finance-2 in Model providers (image has none built-in since v0.22)."
echo

if command -v ollama >/dev/null 2>&1; then
  if [[ -z "${OLLAMA_HOST:-}" ]]; then
    echo "hint: export OLLAMA_HOST=0.0.0.0 so containers can reach Ollama (fallback only)"
  fi
  echo "pulling Ollama fallback chat model qwen2.5:1.5b..."
  ollama pull qwen2.5:1.5b
else
  echo "warning: ollama not found on PATH. Fallback chat unavailable until:"
  echo "  export OLLAMA_HOST=0.0.0.0 && ollama pull qwen2.5:1.5b"
  echo "Demo chat is Mistral; the demo can run without Ollama."
fi
