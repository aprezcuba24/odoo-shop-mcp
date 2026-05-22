#!/usr/bin/env bash
# Generate Pydantic models + httpx client from the order_bridge OpenAPI spec.
# Run from repo root: pnpm run gen:order-bridge-types
# Override URL: OPENAPI_URL=https://... bash scripts/gen-order-bridge-api.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OPENAPI_URL="${OPENAPI_URL:-http://localhost:8069/order_bridge/static/openapi.json}"
SPEC="$ROOT/.cache/order_bridge_openapi.json"
MODELS_OUT="$ROOT/app/app/generated/order_bridge_models.py"
CLIENT_DIR="$ROOT/app/app/generated/order_bridge_client"

mkdir -p "$ROOT/.cache" "$ROOT/app/app/generated"

echo "==> Fetching OpenAPI: $OPENAPI_URL"
curl -fsSL "$OPENAPI_URL" -o "$SPEC"
echo "==> Cached spec: $SPEC ($(wc -c <"$SPEC" | tr -d ' ') bytes)"

if command -v uv >/dev/null 2>&1 && [[ -f "$ROOT/pyproject.toml" ]]; then
  echo "==> uv sync"
  uv sync
  echo "==> Generating Pydantic models -> $MODELS_OUT"
  uv run datamodel-codegen \
    --input "$SPEC" \
    --input-file-type openapi \
    --output "$MODELS_OUT" \
    --no-use-annotated
  echo "==> Generating HTTP client (attrs + httpx) -> $CLIENT_DIR"
  uv run openapi-python-client generate \
    --path "$SPEC" \
    --output-path "$CLIENT_DIR" \
    --meta none \
    --overwrite
else
  if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PY="$ROOT/.venv/bin/python"
  else
    PY="python3"
  fi
  echo "==> Installing generator deps with $PY -m pip"
  "$PY" -m pip install -q "datamodel-code-generator[http]>=0.57.0" "openapi-python-client>=0.28.0"
  echo "==> Generating Pydantic models -> $MODELS_OUT"
  "$PY" -m datamodel_code_generator \
    --input "$SPEC" \
    --input-file-type openapi \
    --output "$MODELS_OUT" \
    --no-use-annotated
  echo "==> Generating HTTP client (attrs + httpx) -> $CLIENT_DIR"
  "$PY" -m openapi_python_client generate \
    --path "$SPEC" \
    --output-path "$CLIENT_DIR" \
    --meta none \
    --overwrite
fi

echo "==> Done."
