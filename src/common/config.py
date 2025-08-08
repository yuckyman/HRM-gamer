from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    log_dir: Path
    rng_seed: int
    debug: bool


def read_config(log_dir_cli: str | None = None, debug_cli: bool | None = None) -> AppConfig:
    log_dir_env = os.getenv("LOG_DIR", "./runs/latest")
    log_dir_str = log_dir_cli or log_dir_env
    rng_seed = int(os.getenv("RNG_SEED", "12345"))
    debug_env = os.getenv("DEBUG", "0") in {"1", "true", "True"}
    debug = bool(debug_cli) if debug_cli is not None else debug_env
    return AppConfig(log_dir=Path(log_dir_str), rng_seed=rng_seed, debug=debug)


def get_llm_keys() -> dict[str, str | None]:
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "claude": os.getenv("CLAUDE_API_KEY"),
    }