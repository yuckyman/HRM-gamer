from __future__ import annotations

from src.common.retro_wrappers import MockPMDEnv
from src.fast.skills.navigation import goto


def test_goto_moves_hero_to_target():
    env = MockPMDEnv(width=8, height=8, rng_seed=1)
    obs, _ = env.reset()
    hero = tuple(obs["map"]["hero"])  # type: ignore
    target = (6, 6)
    grid = [[0 for _ in range(8)] for _ in range(8)]

    actions = goto(target, grid, hero)
    for a in actions:
        obs, _, terminated, truncated, _ = env.step(a)
        assert not truncated
    new_hero = tuple(obs["map"]["hero"])  # type: ignore
    assert new_hero == target