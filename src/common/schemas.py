from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


ALLOWED_GOALS = {"goto", "basic_attack", "kite", "use_item", "exit_dungeon", "wait"}


class Subgoal(BaseModel):
    goal: str
    target: Optional[Dict] = None
    constraints: Optional[Dict] = None
    budget_steps: int = Field(ge=1, le=1000)
    fallback: Optional[Dict] = None

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        if v not in ALLOWED_GOALS:
            raise ValueError(f"goal must be one of {sorted(ALLOWED_GOALS)}")
        return v


class StateSummary(BaseModel):
    map: Dict
    hero: Dict
    inventory: Dict
    flags: Dict
    recent: List[str]
    skills: List[str]