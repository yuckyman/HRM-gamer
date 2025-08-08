from __future__ import annotations

import logging
from typing import Dict, Optional

from pydantic import ValidationError

from ..common.schemas import Subgoal, StateSummary


class FallbackPlanner:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def plan(self, state: StateSummary) -> Subgoal:
        hero = state.hero
        flags = state.flags
        inv = state.inventory
        map_info = state.map

        # Simple heuristics
        if hero.get("hp", 0) < max(5, int(0.2 * hero.get("hp_max", 1))) and inv.get("oran", 0) > 0:
            raw = {"goal": "use_item", "target": {"name": "oran"}, "budget_steps": 3}
        elif flags.get("stairs_visible"):
            target_tile = map_info.get("stairs") or map_info.get("hero")
            raw = {"goal": "goto", "target": {"tile": target_tile}, "budget_steps": 50}
        else:
            raw = {"goal": "wait", "budget_steps": 1}

        try:
            return Subgoal(**raw)
        except ValidationError as e:
            self.logger.warning(f"Fallback planner produced invalid subgoal, coercing to wait: {e}")
            return Subgoal(goal="wait", budget_steps=1)


class LLMClient:
    def __init__(self, openai_key: Optional[str], claude_key: Optional[str], logger: logging.Logger) -> None:
        self.openai_key = openai_key
        self.claude_key = claude_key
        self.logger = logger
        if not openai_key and not claude_key:
            self.logger.warning("No LLM keys found; using fallback planner only.")
        self.fallback = FallbackPlanner(logger)

    def plan_subgoal(self, state: StateSummary) -> Subgoal:
        # For now, always use fallback; plug-in LLM calls later.
        return self.fallback.plan(state)