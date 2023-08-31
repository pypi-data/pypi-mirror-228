from dataclasses import field, dataclass

"""A Renderer is a representation of how a fs should be printed."""


@dataclass
class Renderer:
    """A Renderer provides special instructions for how a fs is displayed."""

    doc_open: str = field(default="")
    doc_close: str = field(default="")
    file_open: str = field(default="")
    file_close: str = field(default="")
    folder_open: str = field(default="")
    folder_close: str = field(default="")


defaultRenderer = Renderer()


markdownRenderer = Renderer(
    '<pre style="line-height:17px">',
    "</pre>",  # Doc open/close
    '<span style="color:gray">',
    "</span>",  # File open/close
)
