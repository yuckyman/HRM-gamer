from __future__ import annotations

from typing import List

from .menu import open_menu, move_cursor, close_menu


def use_item(name: str) -> List[str]:
    # Placeholder deterministic sequence: open menu, move to item, confirm, close.
    seq = []
    seq += open_menu()
    seq += move_cursor(steps=2)
    seq.append("A")
    seq += close_menu()
    return seq