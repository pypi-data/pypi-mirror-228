from __future__ import annotations

import os
import sys
from typing import List, Set

from .constants import PIPE, SPACE_PREFIX, ELBOW, TEE
from .data import Data
from .file import File
from .folder import Folder
from .renderer import Renderer


class DisplayModel:
    def __init__(self, renderer: Renderer):
        self._renderer = renderer
        self._ignore: Set[int] = set()

    def _display_node(self, node: Data) -> str:
        """
        Bookkeeping of nested node depth, node siblings, and order in the queue are
        used to present the FicusSystem in an aesthetic way.
        """

        parts = [PIPE + SPACE_PREFIX for _ in range(node.level)]
        for index in self._ignore:
            if len(parts) > index - 1:
                parts[index - 1] = " " + SPACE_PREFIX

        if parts:
            parts[-1] = ELBOW if node.last is True else TEE

        is_file = isinstance(node, File)
        file_open = self._renderer.file_open if is_file else self._renderer.folder_open
        file_close = (
            self._renderer.file_close if is_file else self._renderer.folder_close
        )

        # checking for Folder type
        end = "\\" if not is_file else ""

        return f'{"".join(parts)}{file_open}{node.name}{file_close}{end}'

    def _display_header(self, header: str) -> int:
        """Writes the CWD to stdout with forward slashes and its length."""

        parts = header.split(os.sep)
        if len(parts) > 1:
            header = f"\\".join(parts[:-1])
            sys.stdout.write(f"{header}\\\n")
            return max(header[1:].find("\\", 1), 0)

        # when root is passed in
        return 0

    def display(self, node: Data, root: str) -> None:
        """Prints the directory structure to stdout."""
        sys.stdout.write(self._renderer.doc_open + "\n")

        header_length = self._display_header(root)
        node.last = True

        q: List[Data] = [node]
        self._ignore = {i for i in range(node.level)}
        while q:
            node = q.pop()
            if node.last is False:
                if node.level in self._ignore:
                    self._ignore.remove(node.level)
            line = self._display_node(node)
            new_line = line.lstrip()

            max_s = max((len(line) - len(new_line)), header_length)

            sys.stdout.write((max_s * " ") + new_line + "\n")
            if node.last is True:
                # track nodes without children.
                self._ignore.add(node.level)

            if isinstance(node, Folder):
                q += node.contents()

        sys.stdout.write(self._renderer.doc_close + "\n")
