#!/usr/bin/env bash
set -euo pipefail

# Linux setup script
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-dev build-essential curl

# uv install (standalone)
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# RetroArch (distro package)
sudo apt-get install -y retroarch || true

uv sync --frozen || uv sync

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Linux setup complete. Activate venv with: source .venv/bin/activate or use 'uv run'"