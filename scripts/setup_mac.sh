#!/usr/bin/env bash
set -euo pipefail

# macOS setup script
# - Installs RetroArch via Homebrew
# - Sets up Python venv and installs deps

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install from https://brew.sh first." >&2
  exit 1
fi

brew install --cask retroarch || true

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "macOS setup complete. Activate venv with: source .venv/bin/activate"