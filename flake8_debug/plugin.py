import ast
from typing import List, Tuple, Generator, Type, Any, Optional

from flake8_debug.errors import ERRORS, Error
from flake8_debug.meta import Meta

TDebug = Generator[Tuple[int, int, str, Type[Any]], None, None]


class DebugVisitor(ast.NodeVisitor):
    def __init__(self, errors: Tuple[Type[Error], ...]) -> None:
        self._errors = errors
        self.issues: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        for error in self._errors:
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == error.func_name
            ) or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == error.func_name
            ):
                self.issues.append((node.lineno, node.col_offset, error().msg))


class NoDebug:
    name: str = Meta.name
    version: str = Meta.version

    def __init__(
        self, tree: ast.Module, filename: Optional[str] = None
    ) -> None:
        self._tree = tree
        self._filename = filename

    def run(self) -> TDebug:
        debug = DebugVisitor(ERRORS)
        debug.visit(self._tree)
        for lineno, column, msg in debug.issues:  # type: int, int, str
            yield lineno, column, msg, type(self)
