from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List

from .common.config import read_config, get_llm_keys
from .common.logging_utils import setup_logging, JsonlSink
from .common.retro_wrappers import make_env
from .fast.runner import FastRunner
from .slow.llm_client import LLMClient
from .slow.manager import SlowManager


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--mock", action="store_true", help="Use mock environment")
    p.add_argument("--episodes", type=int, default=1)
    p.add_argument("--max-steps", type=int, default=200)
    p.add_argument("--log-dir", type=str, default=None)
    p.add_argument("--debug", action="store_true")
    p.add_argument("--env", type=str, default=None, help="Real env game name")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = read_config(log_dir_cli=args.log_dir, debug_cli=args.debug)
    logger = setup_logging(cfg.log_dir, debug=cfg.debug)
    sink = JsonlSink(cfg.log_dir)

    keys = get_llm_keys()
    llm = LLMClient(keys.get("openai"), keys.get("claude"), logger)
    manager = SlowManager(llm, logger)

    env = make_env(mock=args.mock or not args.env, rng_seed=cfg.rng_seed, game_name=args.env)
    runner = FastRunner(env, logger)

    available_skills: List[str] = ["goto(tile)", "basic_attack(dir)", "use_item(name)", "kite(enemy)", "wait"]

    for ep in range(args.episodes):
        obs, info = env.reset()
        logger.info(f"episode {ep+1}/{args.episodes} reset: info={info}")
        recent_events: List[str] = ["new_floor"]
        steps = 0
        total_reward = 0.0
        terminated = truncated = False

        while steps < args.max_steps and not (terminated or truncated):
            summary = manager.summarize(obs, available_skills, recent_events)
            if manager.should_replan(summary, recent_events):
                subgoal = manager.plan(summary).model_dump()
            else:
                subgoal = {"goal": "wait", "budget_steps": 1}

            # Construct a simple grid from map size for mock (all free)
            size = summary.map.get("size", [16, 16])
            width, height = int(size[0]), int(size[1])
            grid = [[0 for _ in range(width)] for _ in range(height)]
            hero = tuple(summary.map.get("hero", [1, 1]))  # type: ignore

            obs, reward, terminated, truncated, info = runner.execute_subgoal(subgoal, grid, hero)
            total_reward += reward or 0.0
            steps += 1

            sink.write({
                "ep": ep,
                "step": steps,
                "subgoal": subgoal,
                "reward": reward,
                "terminated": terminated,
                "truncated": truncated,
                "info": info,
            })

            recent_events = []

        logger.info(f"episode {ep+1} finished: steps={steps} total_reward={total_reward:.3f} term={terminated} trunc={truncated}")


if __name__ == "__main__":
    main()