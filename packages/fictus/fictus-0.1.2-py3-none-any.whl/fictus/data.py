from __future__ import annotations

from typing import Optional


class Data:
    def __init__(self, name: str, parent: Optional[Data] = None):
        self.name = name
        self.last = False

        self._level = 0
        self._parent = parent

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, val: int) -> None:
        self._level = val

    @property
    def parent(self) -> Optional[Data]:
        return self._parent

    @parent.setter
    def parent(self, other: Optional[Data]) -> None:
        self._parent = other

    def __lt__(self, other: Data) -> bool:
        return self.name > other.name
