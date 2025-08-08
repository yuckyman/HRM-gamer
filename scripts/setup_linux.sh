#!/usr/bin/env bash
set -euo pipefail

# Linux setup script
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-dev build-essential retroarch

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Linux setup complete. Activate venv with: source .venv/bin/activate"