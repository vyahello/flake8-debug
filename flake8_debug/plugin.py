import ast
import sys
from typing import Final, Generator

from flake8_debug.errors import ERRORS, Error
from flake8_debug.meta import Meta

TDebug = Generator[tuple[int, int, str, type["NoDebug"]], None, None]

# Func names meaningful only as attribute calls (e.g. pdb.set_trace())
_ATTR_DETECTABLE: Final[frozenset[str]] = frozenset({'set_trace'})
# Only flag attribute calls when the object looks like a known debugger module
_DEBUGGER_MODULES: Final[frozenset[str]] = frozenset({'pdb', 'ipdb'})


class DebugVisitor(ast.NodeVisitor):
    def __init__(self, errors: tuple[type[Error], ...]) -> None:
        self._errors = errors
        self.issues: list[tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        for error in self._errors:
            is_bare_call = (
                isinstance(node.func, ast.Name)
                and node.func.id == error.func_name
            )
            is_attr_call = (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == error.func_name
                and error.func_name in _ATTR_DETECTABLE
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in _DEBUGGER_MODULES
            )
            if is_bare_call or is_attr_call:
                self.issues.append((node.lineno, node.col_offset, error().msg))
        self.generic_visit(node)


class NoDebug:
    name: str = Meta.name
    version: str = Meta.version

    def __init__(self, tree: ast.Module, filename: str | None = None) -> None:
        self._tree = tree
        self._filename = filename

    def run(self) -> TDebug:
        debug = DebugVisitor(ERRORS)
        old_limit = sys.getrecursionlimit()
        try:
            sys.setrecursionlimit(max(old_limit, 2000))
            debug.visit(self._tree)
        except RecursionError:
            pass
        finally:
            sys.setrecursionlimit(old_limit)
        for lineno, column, msg in debug.issues:
            yield lineno, column, msg, type(self)
