from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Iterable, List, Optional, Tuple

Grid = List[List[int]]  # 0=free, 1=blocked
Pos = Tuple[int, int]


def neighbors(pos: Pos, width: int, height: int) -> Iterable[Pos]:
    x, y = pos
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            yield nx, ny


def find_path(grid: Grid, start: Pos, goal: Pos) -> List[Pos]:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    if not (0 <= start[0] < width and 0 <= start[1] < height):
        return []
    if not (0 <= goal[0] < width and 0 <= goal[1] < height):
        return []
    if start == goal:
        return [start]

    queue: Deque[Pos] = deque([start])
    came_from: Dict[Pos, Optional[Pos]] = {start: None}

    def is_free(p: Pos) -> bool:
        x, y = p
        return grid[y][x] == 0

    if not is_free(start) or not is_free(goal):
        return []

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for n in neighbors(current, width, height):
            if n in came_from:
                continue
            if not is_free(n):
                continue
            came_from[n] = current
            queue.append(n)

    if goal not in came_from:
        return []

    # Reconstruct path
    path: List[Pos] = []
    cur: Optional[Pos] = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path