#!/usr/bin/env bash
set -euo pipefail

# prefer uv-run without requiring manual activation
if command -v uv >/dev/null 2>&1; then
  export PYTHONUNBUFFERED=1
  exec uv run python -m src.app "$@"
fi

source .venv/bin/activate
export PYTHONUNBUFFERED=1

python -m src.app "$@"