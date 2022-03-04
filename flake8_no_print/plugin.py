import ast
from typing import List, Tuple, Generator, Type, Any, Optional

from flake8_no_print.meta import Meta


class ForbiddenVisitor(ast.NodeVisitor):
    forbidden = 'print'

    def __init__(self) -> None:
        self.issues: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == self.forbidden:
            message = (
                f'NP100 "{node.func.id}()" function usage '
                'is forbidden, please consider using "logging" module'
            )
            self.issues.append((node.lineno, node.col_offset, message))


class NoPrint:
    name: str = Meta.name
    version: str = Meta.version

    def __init__(
        self, tree: ast.Module, filename: Optional[str] = None
    ) -> None:
        self._tree = tree
        self._filename = filename

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        no_print = ForbiddenVisitor()
        no_print.visit(self._tree)
        for lineno, column, msg in no_print.issues:  # type: int, int, str
            yield lineno, column, msg, type(self)
