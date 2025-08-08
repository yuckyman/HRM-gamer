from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(log_dir: Path, debug: bool = False) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("hrm")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Console handler with Rich
    console = Console(force_terminal=True)
    rich_handler = RichHandler(console=console, show_path=False, rich_tracebacks=True)
    rich_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    logger.addHandler(rich_handler)

    logger.debug(f"Logging initialized. log_dir={log_dir} debug={debug}")
    return logger


class JsonlSink:
    def __init__(self, log_dir: Path, filename: str = "events.jsonl") -> None:
        self.path = log_dir / filename
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")