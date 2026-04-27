import ast
from typing import Tuple
from unittest.mock import patch

import pytest

from flake8_debug.errors import (
    Error,
    PrintError,
    BreakpointError,
    BreakpointHookError,
    PdbError,
)
from flake8_debug.plugin import DebugVisitor, NoDebug

pytestmark = pytest.mark.unit


def _plugin_results(py_content: str) -> Tuple[str, ...]:
    """Run the flake8 plugin on code and format its output."""
    plugin = NoDebug(ast.parse(py_content))
    return tuple(
        f'{line}:{column + 1} {message}'
        for line, column, message, _ in plugin.run()
    )


def _out(line: int, column: int, err: Error) -> str:
    """Format an expected plugin violation line."""
    return f'{line}:{column} {err.msg}'


def test_absent_print() -> None:
    """No print() call should yield no violations."""
    assert not _plugin_results('def f():\n    ...')


def test_present_print() -> None:
    """A single print() call should be reported as DB100."""
    assert _plugin_results('def f():\n    print(0)') == (
        _out(line=2, column=5, err=PrintError()),
    )


def test_present_multiple_prints() -> None:
    """Multiple print() calls should each be reported."""
    assert _plugin_results('def f():\n    print(0)\n    print(0)') == tuple(
        _out(line, column=5, err=PrintError()) for line in (2, 3)
    )


def test_absent_breakpoint() -> None:
    """No breakpoint() call should yield no violations."""
    assert not _plugin_results('def f():\n    ...')


def test_present_breakpoint() -> None:
    """A single breakpoint() call should be reported as DB200."""
    assert _plugin_results('def f():\n    breakpoint(0)') == (
        _out(line=2, column=5, err=BreakpointError()),
    )


def test_present_multiple_breakpoints() -> None:
    """Multiple breakpoint() calls should each be reported."""
    assert _plugin_results(
        'def f():\n    breakpoint(0)\n    breakpoint(0)'
    ) == tuple(_out(line, column=5, err=BreakpointError()) for line in (2, 3))


def test_absent_breakpointhook() -> None:
    """No breakpointhook() call should yield no violations."""
    assert not _plugin_results('def f():\n    ...')


def test_present_breakpointhook() -> None:
    """A breakpointhook() call should be reported as DB201."""
    assert _plugin_results(
        'def f():\n    from sys import breakpointhook\n    breakpointhook(0)'
    ) == (
        _out(line=3, column=5, err=BreakpointHookError()),
    )


def test_present_multiple_breakpointhooks() -> None:
    """Multiple breakpointhook() calls should each be reported."""
    assert _plugin_results(
        'def f():\n    from sys import breakpointhook\n    '
        'breakpointhook(0)\n    breakpointhook(0)'
    ) == tuple(
        _out(line, column=5, err=BreakpointHookError()) for line in (3, 4)
    )


def test_present_set_trace() -> None:
    """A pdb.set_trace() call should be reported as DB300."""
    assert _plugin_results(
        'def f():\n    import pdb\n    pdb.set_trace()'
    ) == (
        _out(line=3, column=5, err=PdbError()),
    )


def test_present_bare_set_trace() -> None:
    """A bare set_trace() call should be reported as DB300."""
    assert _plugin_results(
        'def f():\n    from pdb import set_trace\n    set_trace()'
    ) == (
        _out(line=3, column=5, err=PdbError()),
    )


def test_nested_print_is_detected() -> None:
    """Nested print() calls (as call args) should be reported."""
    assert _plugin_results('foo(print(0))') == (
        _out(line=1, column=5, err=PrintError()),
    )


def test_nested_breakpoint_is_detected() -> None:
    """Nested breakpoint() calls (as call args) should be reported."""
    assert _plugin_results('foo(breakpoint())') == (
        _out(line=1, column=5, err=BreakpointError()),
    )


def test_no_false_positive_on_arbitrary_object_print() -> None:
    """Attribute calls named print() should not be treated as builtins.print()."""
    assert not _plugin_results('logger.print("msg")')


def test_no_false_positive_on_arbitrary_object_breakpoint() -> None:
    """Attribute calls named breakpoint() should not be treated as builtins.breakpoint()."""
    assert not _plugin_results('self.breakpoint()')


def test_no_false_positive_on_arbitrary_object_set_trace() -> None:
    """Attribute calls named set_trace() should not be treated as pdb.set_trace()."""
    assert not _plugin_results('cursor.set_trace()')


def test_recursion_error_is_handled() -> None:
    """A RecursionError in AST traversal should not crash flake8."""
    tree = ast.parse('x = 1')
    with patch.object(DebugVisitor, 'visit', side_effect=RecursionError):
        assert list(NoDebug(tree).run()) == []
