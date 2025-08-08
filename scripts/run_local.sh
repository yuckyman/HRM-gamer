#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
export PYTHONUNBUFFERED=1

python -m src.app "$@"