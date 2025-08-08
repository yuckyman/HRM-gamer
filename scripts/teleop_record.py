#!/usr/bin/env python3
import argparse
from pathlib import Path

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "L", "R", "START", "SELECT", "WAIT"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("teleop_actions.txt"))
    args = parser.parse_args()

    content = "\n".join(["# Teleop sequence (edit manually)"] + ACTIONS)
    args.out.write_text(content)
    print(f"Wrote template actions to {args.out}")

if __name__ == "__main__":
    main()