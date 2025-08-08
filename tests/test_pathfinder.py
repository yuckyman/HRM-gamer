from __future__ import annotations

from src.fast.planner.pathfinder import find_path


def test_find_path_simple():
    grid = [[0 for _ in range(10)] for _ in range(10)]
    start = (0, 0)
    goal = (9, 9)
    path = find_path(grid, start, goal)
    assert path[0] == start
    assert path[-1] == goal
    assert len(path) > 0


def test_find_path_obstacle():
    grid = [[0 for _ in range(10)] for _ in range(10)]
    # vertical wall with a gap
    for y in range(10):
        grid[y][5] = 1
    grid[5][5] = 0
    start = (2, 2)
    goal = (8, 2)
    path = find_path(grid, start, goal)
    assert path[0] == start
    assert path[-1] == goal
    # ensure it routes through the gap
    assert (5, 5) in path