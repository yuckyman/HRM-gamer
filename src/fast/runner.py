from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from .skills.navigation import goto as goto_skill
from .skills.combat import basic_attack


class FastRunner:
    def __init__(self, env, logger: logging.Logger) -> None:
        self.env = env
        self.logger = logger

    def step_actions(self, actions: List[str]):
        obs_acc = None
        info_last: Dict = {}
        total_reward = 0.0
        terminated = truncated = False
        for a in actions:
            obs, reward, terminated, truncated, info = self.env.step(a)
            self.logger.debug(f"fast: action={a} reward={reward:.3f} term={terminated} trunc={truncated} info={info}")
            obs_acc = obs
            info_last = info
            total_reward += reward
            if terminated or truncated:
                break
        return obs_acc, total_reward, terminated, truncated, info_last

    def execute_subgoal(self, subgoal: Dict, grid: List[List[int]], hero: Tuple[int, int]):
        goal = subgoal.get("goal")
        if goal == "goto":
            tile = tuple(subgoal.get("target", {}).get("tile", hero))  # type: ignore
            actions = goto_skill(tile, grid, hero)
        elif goal == "basic_attack":
            actions = basic_attack()
        elif goal == "wait":
            actions = ["WAIT"]
        else:
            actions = ["WAIT"]
        return self.step_actions(actions)