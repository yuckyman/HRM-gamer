from __future__ import annotations

from typing import List, Tuple

from ..planner.pathfinder import find_path


DIR_TO_ACTION = {
    (0, -1): "UP",
    (0, 1): "DOWN",
    (-1, 0): "LEFT",
    (1, 0): "RIGHT",
}


def goto(tile: Tuple[int, int], grid: List[List[int]], hero: Tuple[int, int]) -> List[str]:
    path = find_path(grid, hero, tile)
    actions: List[str] = []
    if not path:
        return actions
    # path includes start; convert successive diffs to actions
    for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
        dx, dy = x1 - x0, y1 - y0
        action = DIR_TO_ACTION.get((dx, dy))
        if action is None:
            raise ValueError(f"Non-Manhattan step in path: {(dx, dy)}")
        actions.append(action)
    return actions