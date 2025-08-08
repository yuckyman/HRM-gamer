# Reasoning Prompts (stub)

System prompt goals:
- Produce a valid Subgoal JSON every time (strict schema).
- Prefer safety (survive) > progress (stairs) > loot.

User prompt template outline:
- Provide compact state summary
- Provide available skills
- Ask for subgoal within step budget

See `src/slow/prompt_templates.py` for the concrete templates used by the manager.