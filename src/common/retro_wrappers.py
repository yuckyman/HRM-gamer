from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple
import random


ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "L", "R", "START", "SELECT", "WAIT"]


@dataclass
class Observation:
    map: Dict[str, Any]
    hero: Dict[str, Any]
    inventory: Dict[str, int]
    flags: Dict[str, bool]


class MockPMDEnv:
    def __init__(self, width: int = 16, height: int = 16, rng_seed: int = 12345) -> None:
        self.width = width
        self.height = height
        self.random = random.Random(rng_seed)
        self.reset()

    def reset(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        self.step_count = 0
        self.floor = 1
        self.hero_x = 1
        self.hero_y = 1
        self.hp_max = 45
        self.hp = 30
        self.belly = 50
        self.stairs = (self.width - 2, self.height - 2)
        self.in_menu = False
        self.stairs_visible = True
        obs = self._obs()
        info = {"event": "reset"}
        return obs, info

    def _obs(self) -> Dict[str, Any]:
        return {
            "map": {
                "floor": self.floor,
                "size": [self.width, self.height],
                "stairs": [self.stairs[0], self.stairs[1]],
                "hero": [self.hero_x, self.hero_y],
            },
            "hero": {"hp": self.hp, "hp_max": self.hp_max, "belly": self.belly, "status": "normal"},
            "inventory": {"oran": 1, "apple": 1, "escape_orb": 1},
            "flags": {"in_menu": self.in_menu, "stairs_visible": self.stairs_visible},
        }

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        assert action in ACTIONS, f"Unknown action {action}"
        self.step_count += 1
        reward = -0.01
        terminated = False
        truncated = False
        info: Dict[str, Any] = {}

        if action == "UP":
            self.hero_y = max(0, self.hero_y - 1)
        elif action == "DOWN":
            self.hero_y = min(self.height - 1, self.hero_y + 1)
        elif action == "LEFT":
            self.hero_x = max(0, self.hero_x - 1)
        elif action == "RIGHT":
            self.hero_x = min(self.width - 1, self.hero_x + 1)
        elif action == "A":
            info["attack"] = True
            reward += 0.0
        elif action == "WAIT":
            reward += 0.0

        if (self.hero_x, self.hero_y) == self.stairs:
            reward += 1.0
            terminated = True
            info["reached_stairs"] = True

        if self.step_count >= 1000:
            truncated = True

        return self._obs(), reward, terminated, truncated, info

    def render(self) -> None:
        pass


class RealRetroEnvWrapper:
    def __init__(self, game_name: str) -> None:
        # Lazy import to avoid dependency in mock mode
        try:
            import retro  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("stable-retro/retro not available. Install stable-retro to use real env.") from exc
        self.retro = retro  # keep reference
        self.env = retro.make(game=game_name)

    def reset(self):  # pragma: no cover - intended for real env runtime
        return self.env.reset()

    def step(self, action: str):  # pragma: no cover
        raise NotImplementedError("Map button strings to emulator button arrays here.")

    def render(self):  # pragma: no cover
        return self.env.render()


def make_env(mock: bool = True, rng_seed: int = 12345, game_name: str | None = None):
    if mock or game_name is None:
        return MockPMDEnv(rng_seed=rng_seed)
    return RealRetroEnvWrapper(game_name)