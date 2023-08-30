from .content import ContentManager as ContentManager
from .naming import Naming as Naming
from .processor import Processor as Processor
from typing import Any

class Compiler:
    @staticmethod
    def load(path: str) -> dict[str, dict[str, dict[str, Any]]]: ...
    @classmethod
    def compile(cls, path: str, out_dir: str | None = ...) -> None: ...
    @classmethod
    def decompile(cls, _data: dict[str, dict[str, dict[str, Any]]], out: str) -> None: ...
