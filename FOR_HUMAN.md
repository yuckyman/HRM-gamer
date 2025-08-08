## How to Run This Project (Human Runbook)

This guide explains environment variables, installation, and running both mock mode and emulator mode. It also shows how to get lots of debug output.

### Environment Variables
Set in `.env` or your shell. Copy `.env.example` to `.env` to start.

- `OPENAI_API_KEY`: Optional. Enables the LLM manager (OpenAI). If unset, a mock planner is used.
- `CLAUDE_API_KEY`: Optional. Enables Anthropic client. If unset, a mock planner is used.
- `LOG_DIR`: Optional. Defaults to `./runs/latest`. Where logs (JSONL) and screenshots are written.
- `RNG_SEED`: Optional. Integer seed for determinism in mock mode.

### Install (Linux)
```bash
# 1) System deps (RetroArch optional for emulator mode)
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-dev build-essential retroarch

# 2) Python venv + deps
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3) Env vars (optional LLM)
cp .env.example .env
# edit .env and set OPENAI_API_KEY / CLAUDE_API_KEY if desired
```

### Install (macOS)
```bash
# 1) RetroArch (mGBA core) + Python
brew install --cask retroarch
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

### Running
- Mock mode (no ROM needed, rich debug logs):
```bash
source .venv/bin/activate
python -m src.app --mock --episodes 1 --max-steps 200 --log-dir runs/dev
```

- Emulator mode (requires your PMD: Red Rescue Team ROM and stable-retro):
```bash
# Ensure stable-retro can find ROM (place ROM under RetroArch content dirs) and JSON integrations in env/retro-integration/
source .venv/bin/activate
python -m src.app --env Game="PokemonMysteryDungeonRedRescueTeam-GBA" --max-steps 200
```

### Debug Output
- Console: Rich, colorized logs at DEBUG level.
- Files: JSONL event logs under `LOG_DIR` (default `runs/latest/events.jsonl`).
- Screenshots: PNGs saved periodically under `LOG_DIR/screens/` in emulator mode.
- Savestates: Optional; see `src/common/retro_wrappers.py`.

To increase verbosity:
```bash
python -m src.app --mock --debug
```

### Tests
```bash
pytest -q
```

### Troubleshooting
- Missing deps: run `scripts/setup_linux.sh` (Linux) or `scripts/setup_mac.sh` (macOS).
- No ROM found: use mock mode, or add your ROM to RetroArch content folders. Verify integration JSON names match.
- LLM keys missing: the manager uses a rule-based fallback and logs a warning. Set `OPENAI_API_KEY` or `CLAUDE_API_KEY` to enable LLM planning.

### Legal
Supply your own legally-dumped ROM. Do not commit ROMs here. Integration files only include hashes and metadata.