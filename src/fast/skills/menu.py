from __future__ import annotations

from typing import List


def open_menu() -> List[str]:
    return ["START"]


def close_menu() -> List[str]:
    return ["B"]


def move_cursor(steps: int) -> List[str]:
    action = "DOWN" if steps >= 0 else "UP"
    return [action for _ in range(abs(steps))]