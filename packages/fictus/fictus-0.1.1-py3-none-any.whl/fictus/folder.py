from __future__ import annotations
from typing import List, Union, Sequence, Optional

from .data import Data
from .file import File


class Folder(Data):
    """
    A Folder is a data item in the FictusSystem that may contain other Folders
    and/or Files.
    """

    def __init__(self, name: str, parent: Optional[Folder] = None):
        super().__init__(name, parent)

        self._folders: List[Folder] = []
        self._files: List[File] = []

    def file(self, file: File) -> None:
        """Adds a file to the current Folder."""
        file.level = self._level + 1
        self._files.append(file)

    def files(self) -> List[File]:
        """Returns an alphabetized list of files found in the current Folder."""
        return sorted(self._files[::])

    def folder(self, folder: Folder) -> None:
        """Adds a direct sub-folder to the current Folder."""
        folder.parent = self
        folder._level = self._level + 1
        self._folders.append(folder)

    def folders(self) -> List[Folder]:
        """Returns an alphabetized list of folders found in the current Folder."""
        return sorted(self._folders[::])

    def contents(self) -> Sequence[Union[File, Folder]]:
        """Returns an alphabetized list of folders and files found in the current Folder."""
        items: List[Union[File, Folder]] = []
        items += sorted(self._files[::])
        items += sorted(self._folders[::])
        if items:
            items[0].last = True
        return items
