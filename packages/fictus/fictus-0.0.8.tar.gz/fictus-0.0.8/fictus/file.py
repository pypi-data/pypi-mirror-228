from __future__ import annotations

from .data import Data


class File(Data):
    def __init__(self, name: str):
        super().__init__(name)
