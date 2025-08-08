#!/usr/bin/env bash
set -euo pipefail

# macOS setup script
# - Installs RetroArch via Homebrew
# - Installs uv and syncs deps into .venv

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install from https://brew.sh first." >&2
  exit 1
fi

brew install uv || true
brew install --cask retroarch || true

uv sync --frozen || uv sync

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "macOS setup complete. Activate venv with: source .venv/bin/activate or use 'uv run'"