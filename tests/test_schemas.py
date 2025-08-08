from __future__ import annotations

import pytest

from src.common.schemas import Subgoal, StateSummary


def test_state_summary_example():
    payload = {
        "map": {"floor": 4, "size": [56, 56], "stairs": [12, 33], "hero": [8, 30]},
        "hero": {"hp": 18, "hp_max": 45, "belly": 42, "status": "normal"},
        "inventory": {"oran": 1, "apple": 1, "escape_orb": 1},
        "flags": {"in_menu": False, "stairs_visible": True},
        "recent": ["enemy_adjacent_west", "took_8_damage"],
        "skills": ["goto(tile)", "basic_attack(dir)", "use_item(name)", "kite(enemy)"],
    }
    s = StateSummary(**payload)
    assert s.map["floor"] == 4
    assert len(s.skills) == 4


def test_subgoal_bounds():
    Subgoal(goal="wait", budget_steps=1)
    Subgoal(goal="goto", budget_steps=1000)
    with pytest.raises(Exception):
        Subgoal(goal="goto", budget_steps=0)
    with pytest.raises(Exception):
        Subgoal(goal="goto", budget_steps=1001)


def test_subgoal_goal_enum():
    Subgoal(goal="goto", budget_steps=10)
    with pytest.raises(Exception):
        Subgoal(goal="fly", budget_steps=10)