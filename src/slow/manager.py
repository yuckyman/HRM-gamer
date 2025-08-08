from __future__ import annotations

import logging
from typing import Dict, List

from pydantic import ValidationError

from ..common.schemas import StateSummary, Subgoal
from .llm_client import LLMClient


class SlowManager:
    def __init__(self, llm: LLMClient, logger: logging.Logger) -> None:
        self.llm = llm
        self.logger = logger
        self._last_floor: int | None = None

    def should_replan(self, summary: StateSummary, recent_events: List[str]) -> bool:
        floor = int(summary.map.get("floor", 0))
        if self._last_floor is None or floor != self._last_floor:
            self._last_floor = floor
            return True
        if summary.hero.get("hp", 9999) < max(5, int(0.2 * summary.hero.get("hp_max", 1))):
            return True
        if summary.flags.get("stairs_visible", False):
            return True
        if any(ev in {"no_progress"} for ev in recent_events):
            return True
        return False

    def summarize(self, obs: Dict, available_skills: List[str], recent_events: List[str]) -> StateSummary:
        # Obs is already a compact dict in our mock env.
        summary = StateSummary(
            map=obs.get("map", {}),
            hero=obs.get("hero", {}),
            inventory=obs.get("inventory", {}),
            flags=obs.get("flags", {}),
            recent=recent_events,
            skills=available_skills,
        )
        return summary

    def plan(self, summary: StateSummary) -> Subgoal:
        try:
            sg = self.llm.plan_subgoal(summary)
            self.logger.info(f"slow: subgoal={sg.model_dump()}")
            return sg
        except ValidationError as e:
            self.logger.warning(f"Subgoal validation error: {e}")
            return Subgoal(goal="wait", budget_steps=1)