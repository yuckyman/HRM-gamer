# HRM-gamer: Hierarchical Agent for Pokémon Mystery Dungeon (GBA)

This repository scaffolds a hierarchical "X plays Pokémon" agent for Pokémon Mystery Dungeon: Red Rescue Team (GBA), using a slow planning stream (LLM manager) and a fast execution stream (skills + pathing). It is designed to run headless with stable-retro + mGBA and includes mock fallbacks for development without a ROM.

- Slow stream: subgoal planning (LLM; JSON schema enforced)
- Fast stream: button-level skills (deterministic)
- Environment: stable-retro (Gym Retro fork) + libretro mGBA core

See `FOR_HUMAN.md` for detailed setup, env vars, and running instructions.

## Layout
- `src/`: code
- `env/retro-integration/`: integration files (ROM metadata, RAM slices)
- `scripts/`: setup and run scripts
- `tests/`: unit tests for schemas, pathfinder, and skills
- `docs/`: notes and prompts

## Quickstart (mock mode)
```bash
# with uv
uv sync
python -m src.app --mock
```

## Tests
```bash
uv run pytest -q
```

Legal: You must supply your own legally dumped ROM. Integration files reference ROM hashes for environment loading. Do not commit ROMs.