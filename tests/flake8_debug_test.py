import ast
from typing import Tuple

import pytest

from flake8_debug.errors import (
    Error,
    PrintError,
    BreakpointError,
    BreakpointHookError,
    PdbError,
)
from flake8_debug.plugin import NoDebug

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
