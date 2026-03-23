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
    plugin = NoDebug(ast.parse(py_content))
    return tuple(
        f'{line}:{column + 1} {message}'
        for line, column, message, _ in plugin.run()
    )


def _out(line: int, column: int, err: Error) -> str:
    return f'{line}:{column} {err.msg}'


def test_absent_print():
    assert not _plugin_results('def f():\n    ...')


def test_present_print():
    assert _plugin_results('def f():\n    print(0)') == (
        _out(line=2, column=5, err=PrintError()),
    )


def test_present_multiple_prints():
    assert _plugin_results('def f():\n    print(0)\n    print(0)') == tuple(
        _out(line, column=5, err=PrintError()) for line in (2, 3)
    )


def test_absent_breakpoint():
    assert not _plugin_results('def f():\n    ...')


def test_present_breakpoint():
    assert _plugin_results('def f():\n    breakpoint(0)') == (
        _out(line=2, column=5, err=BreakpointError()),
    )


def test_present_multiple_breakpoints():
    assert _plugin_results(
        'def f():\n    breakpoint(0)\n    breakpoint(0)'
    ) == tuple(_out(line, column=5, err=BreakpointError()) for line in (2, 3))


def test_absent_breakpointhook():
    assert not _plugin_results('def f():\n    ...')


def test_present_breakpointhook():
    assert _plugin_results(
        'def f():\n    from sys import breakpointhook\n    breakpointhook(0)'
    ) == (
        _out(line=3, column=5, err=BreakpointHookError()),
    )


def test_present_multiple_breakpointhooks():
    assert _plugin_results(
        'def f():\n    from sys import breakpointhook\n    '
        'breakpointhook(0)\n    breakpointhook(0)'
    ) == tuple(
        _out(line, column=5, err=BreakpointHookError()) for line in (3, 4)
    )


def test_present_set_trace():
    assert _plugin_results(
        'def f():\n    import pdb\n    pdb.set_trace()'
    ) == (
        _out(line=3, column=5, err=PdbError()),
    )


def test_present_bare_set_trace():
    assert _plugin_results(
        'def f():\n    from pdb import set_trace\n    set_trace()'
    ) == (
        _out(line=3, column=5, err=PdbError()),
    )


def test_nested_print_is_detected():
    assert _plugin_results('foo(print(0))') == (
        _out(line=1, column=5, err=PrintError()),
    )


def test_nested_breakpoint_is_detected():
    assert _plugin_results('foo(breakpoint())') == (
        _out(line=1, column=5, err=BreakpointError()),
    )


def test_no_false_positive_on_arbitrary_object_print():
    assert not _plugin_results('logger.print("msg")')


def test_no_false_positive_on_arbitrary_object_breakpoint():
    assert not _plugin_results('self.breakpoint()')


def test_no_false_positive_on_arbitrary_object_set_trace():
    assert not _plugin_results('cursor.set_trace()')


def test_recursion_error_is_handled():
    tree = ast.parse('x = 1')
    with patch.object(DebugVisitor, 'visit', side_effect=RecursionError):
        assert list(NoDebug(tree).run()) == []
