import os.path
from typing import Set, Optional

from .displaymodel import DisplayModel
from .fictusexception import FictusException
from .file import File
from .folder import Folder
from .renderer import defaultRenderer


class FictusFileSystem:
    """A FictusFileSystem represent a fake file system (FFS)."""

    DEFAULT_ROOT_NAME = "\\"

    def __init__(self, name=DEFAULT_ROOT_NAME) -> None:
        self.level: int = 0
        self.root: Folder = Folder(name)
        self.current: Folder = self.root
        self._display_model: Optional[DisplayModel] = None

    def set_display_model(self, display) -> None:
        self._display_model = display

    def display(self) -> None:
        if self._display_model is None:
            self._display_model = DisplayModel(defaultRenderer)

        self._display_model.display(self.current, self.cwd())

    @staticmethod
    def _normalize(path: str) -> str:
        return os.path.normpath(path.replace("\\", "/"))

    def mkdir(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and adds the directories
        one at a time."""
        if not path:
            raise FictusException("A Folder must contain a non-empty string.")

        # hold onto the current directory
        current = self.current
        current_level = self.level

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()

        visited = {d.name: d for d in self.current.folders()}

        for part in normalized_path.split(os.sep):
            if not part:
                continue

            if part not in visited:
                visited[part] = Folder(part)
                self.current.folder(visited[part])

            self.cd(visited[part].name)
            visited = {d.name: d for d in self.current.folders()}

        # return to starting directory
        self.current = current
        self.level = current_level

    def mkfile(self, *files: str) -> None:
        """Takes one or more filenames and adds them to the cwd."""
        visited: Set[str] = {f.name for f in self.current.files()}
        for file in files:
            if not file:
                raise FictusException("A File must contain a non-empty string.")

            if file not in visited:
                visited.add(file)
                self.current.file(File(file))

    def rename(self, old: str, new: str) -> None:
        """Renames a File or Folder based on its name."""
        for content in self.current.contents():
            if content.name == old:
                content.name = new
                break

    def cwd(self):
        """Prints the current working directory."""
        r = []
        visited = set()
        q = [self.current]
        while q:
            n = q.pop()
            if n.name is not None:
                r.append(n.name)
            visited.add(n)
            if n.parent and n.parent not in visited:
                q.append(n.parent)

        return f"{os.sep}".join(r[::-1])

    def _to_root(self) -> None:
        self.current = self.root

    def cd(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and changes the current"""

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()

        for index, part in enumerate(normalized_path.split(os.sep)):
            if not part:
                continue

            if index == 0 and part == self.root.name:
                self._to_root()
                continue

            if part == "..":
                if self.current.parent is None:
                    raise FictusException(
                        f"Folder not accessible; Attempted to move {part} from {self.cwd()}."
                    )
                self.current = self.current.parent
                self.level = self.current.level
            else:
                hm = {f.name: f for f in self.current.folders()}
                if part not in hm:
                    raise FictusException(
                        f"Folder not accessible; Attempted to move {part} from {self.cwd()}."
                    )
                self.current = hm[part]
                self.level = self.current.level

        return None
