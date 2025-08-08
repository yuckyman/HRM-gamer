## X Plays Pokémon — PMD (GBA) Hierarchical Agent

A build plan for a hierarchical “X plays pokémon” agent that plays Pokémon Mystery Dungeon: Red Rescue Team (GBA). Designed to be agent-friendly for Cursor: explicit tasks, file paths, JSON schemas, and acceptance criteria.

### architecture snapshot
- **slow stream (manager, 0.5–2 Hz)**: subgoal planning over long horizons; LLM-backed with strict JSON schema; event-triggered.
- **fast stream (worker, 10–20 Hz)**: skill executor for button-level control; pathing, micro-combat, menu ops; deterministic.
- **environment**: stable-retro (Gym Retro fork) + libretro `mGBA` core; headless stepping; frame buffer; RAM features.

### repo layout (planned)
```
HRM-gamer/
  docs/
    pmd_ram_notes.md
    reasoning_prompts.md
  env/
    retro-integration/
      PokemonMysteryDungeonRedRescueTeam-GBA.json
      data.json               # RAM slices + labels (iterative)
  src/
    common/
      config.py
      schemas.py
      events.py
      logging_utils.py
      retro_wrappers.py
    fast/
      skills/
        navigation.py
        combat.py
        menu.py
        items.py
      planner/
        pathfinder.py
      runner.py               # fast worker loop
    slow/
      llm_client.py
      manager.py              # slow manager loop
      prompt_templates.py
    app.py                    # orchestrator: wires slow+fast+env
  scripts/
    setup_mac.sh
    run_local.sh
    teleop_record.py
  tests/
    test_schemas.py
    test_pathfinder.py
    test_skills.py
  .env.example
  requirements.txt
  README.md
```

### environment + setup (macOS)
```bash
# 1) python
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip

# 2) python deps (initial)
pip install gymnasium numpy opencv-python stable-retro==0.8.1 pydantic rich tenacity

# 3) RetroArch + mGBA core (via Homebrew)
brew install --cask retroarch
# Inside RetroArch, install the mGBA core once interactively (or place the core in the cores dir)

# 4) keys (optional LLM)
cp .env.example .env
# export OPENAI_API_KEY=...  CLAUDE_API_KEY=...
```

### slow/fast interfaces (contracts)
- slow manager input: compact state summary + recent events + available skills
- slow manager output: a strict subgoal JSON
- fast worker input: subgoal JSON
- fast worker output: actions (buttons) and events back to manager

#### subgoal schema (strict)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Subgoal",
  "type": "object",
  "required": ["goal", "budget_steps"],
  "properties": {
    "goal": {"type": "string", "enum": ["goto", "basic_attack", "kite", "use_item", "exit_dungeon", "wait"]},
    "target": {
      "type": "object",
      "properties": {
        "tile": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
        "name": {"type": "string"}
      }
    },
    "constraints": {
      "type": "object",
      "properties": {
        "avoid_enemies": {"type": "boolean"},
        "min_hp": {"type": "integer"},
        "conserve_items": {"type": "boolean"}
      }
    },
    "budget_steps": {"type": "integer", "minimum": 1, "maximum": 1000},
    "fallback": {"type": "object"}
  }
}
```

#### state summary example (input to LLM)
```json
{
  "map": {"floor": 4, "size": [56,56], "stairs": [12,33], "hero": [8,30]},
  "hero": {"hp": 18, "hp_max": 45, "belly": 42, "status": "normal"},
  "inventory": {"oran": 1, "apple": 1, "escape_orb": 1},
  "flags": {"in_menu": false, "stairs_visible": true},
  "recent": ["enemy_adjacent_west", "took_8_damage"],
  "skills": ["goto(tile)", "basic_attack(dir)", "use_item(name)", "kite(enemy)"]
}
```

### tasks (scaffold — agent friendly)

#### milestone 0 — bootstrap env
- [ ] Create `requirements.txt` with pinned versions (see Setup block)
- [ ] Add `scripts/setup_mac.sh` to automate brew + venv + deps
- [ ] Add `.env.example` with `OPENAI_API_KEY`, `CLAUDE_API_KEY`
- [ ] Add `README.md` with run instructions

#### milestone 1 — stable-retro integration
- [ ] Create `env/retro-integration/PokemonMysteryDungeonRedRescueTeam-GBA.json` (buttons, hashes)
- [ ] Create `env/retro-integration/data.json` exposing minimal RAM:
  - [ ] hero hp, hp_max
  - [ ] floor id, hero grid (x,y)
  - [ ] in_menu flag
  - [ ] stairs visible flag (placeholder; iterative)
- [ ] Implement `src/common/retro_wrappers.py` with: make_env(), frame_skip, savestates, deterministic seed
- [ ] Implement `src/common/schemas.py` with Pydantic models for StateSummary, Subgoal

#### milestone 2 — fast stream (skills + runner)
- [ ] Implement `src/fast/skills/navigation.py` with BFS/A* `goto(tile)` on RAM grid
- [ ] Implement `src/fast/skills/combat.py` with adjacent-attack and simple kite
- [ ] Implement `src/fast/skills/menu.py` deterministic cursor ops
- [ ] Implement `src/fast/skills/items.py` with `use_item(name)` (Oran)
- [ ] Implement `src/fast/planner/pathfinder.py` grid utils
- [ ] Implement `src/fast/runner.py` main loop: consume subgoal, produce button presses, emit events

#### milestone 3 — slow stream (LLM manager)
- [ ] Implement `src/slow/llm_client.py` (OpenAI + Claude adapters)
- [ ] Implement `src/slow/prompt_templates.py` with system + user templates
- [ ] Implement `src/slow/manager.py` event-driven planner: on triggers (new floor, low HP, stairs visible) call LLM, validate JSON, set subgoal

#### milestone 4 — orchestrator + CLI
- [ ] Implement `src/app.py` wiring env + fast worker + slow manager (threads/async)
- [ ] Add `scripts/run_local.sh` to launch
- [ ] Add basic telemetry in `src/common/logging_utils.py` (JSONL)

#### milestone 5 — tests
- [ ] `tests/test_schemas.py` ensures subgoal/state schema validity
- [ ] `tests/test_pathfinder.py` unit tests on synthetic grids
- [ ] `tests/test_skills.py` smoke test press sequences (mock env)

### mvp acceptance criteria
- Can load PMD RRT via stable-retro + mGBA headlessly on macOS
- Fast worker executes: step, goto(tile), basic_attack, use_item(oran)
- Slow manager triggers on: floor entry, low HP, stairs visible; emits valid subgoals JSON 100% of calls
- Agent clears multiple early floors with rule-based micro + LLM goals
- Logs actions, events, and periodic screenshots; can replay from savestates

### triggers (when to call slow manager)
- new floor detected
- hp below threshold or status condition
- stairs become visible
- inventory threshold crossed (e.g., 0 Oran, 0 Apple)
- every N steps without progress

### rewards (for later RL phases)
- distance-to-stairs shaping, survival bonus, damage dealt, item pickups, penalties for traps/status

### risk notes + mitigations
- RAM map gaps → iterative savestate diffing; vision fallback for stairs; add to `docs/pmd_ram_notes.md`
- emulator determinism → fix core to mGBA; lock seeds; disable run-ahead
- LLM stability → strict JSON schema + validator; clamp to safe defaults on invalid outputs

### command snippets
```bash
# run orchestrator
source .venv/bin/activate
python -m src.app

# unit tests
pytest -q
```

### file stubs (to create)
```python
# src/common/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict

class Subgoal(BaseModel):
    goal: str
    target: Optional[Dict] = None
    constraints: Optional[Dict] = None
    budget_steps: int = Field(ge=1, le=1000)
    fallback: Optional[Dict] = None

class StateSummary(BaseModel):
    # minimal; expand over time
    map: Dict
    hero: Dict
    inventory: Dict
    flags: Dict
    recent: List[str]
    skills: List[str]
```

```python
# src/app.py (outline)
def main():
    # wire env, fast runner, slow manager
    ...

if __name__ == "__main__":
    main()
```

### notes on ROM/legal
You must supply your own legally-dumped ROM. Integration files reference ROM hashes for environment loading.

### stretch goals
- teammate policy; inventory economy; trap prediction; map memory across floor
- imitation learning + PPO fine-tuning for micro

### owner’s checklist (you)
- [ ] Provide ROM (don’t commit)
- [ ] Confirm OpenAI/Claude keys or prefer Ollama
- [ ] Approve Homebrew RetroArch install



