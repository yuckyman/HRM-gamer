from __future__ import annotations

from typing import List, Tuple


def basic_attack(direction: Tuple[int, int] | None = None) -> List[str]:
    # GBA generally uses 'A' for confirm/attack.
    return ["A"]


def kite(enemy_pos: Tuple[int, int], hero_pos: Tuple[int, int]) -> List[str]:
    # Very simple: step away once, then attack.
    dx = hero_pos[0] - enemy_pos[0]
    dy = hero_pos[1] - enemy_pos[1]
    step: str
    if abs(dx) >= abs(dy):
        step = "RIGHT" if dx >= 0 else "LEFT"
    else:
        step = "DOWN" if dy >= 0 else "UP"
    return [step, "A"]