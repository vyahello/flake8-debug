import ast
from typing import Tuple

import pytest

from flake8_no_print.plugin import NoPrint

pytestmark = pytest.mark.unit


def _plugin_results(py_content: str) -> Tuple[str, ...]:
    plugin = NoPrint(ast.parse(py_content))
    return tuple(
        f'{line}:{column + 1} {message}'
        for line, column, message, _ in plugin.run()
    )


def _out(line: int, column: int) -> str:
    return (
        f'{line}:{column} NP100 "print()" function usage is forbidden, '
        'please consider using "logging" module'
    )


def test_absent_print():
    assert not _plugin_results('def f():\n    ...')


def test_present_print():
    assert _plugin_results('def f():\n    print(0)') == (
        _out(line=2, column=5),
    )


def test_present_multiple_prints():
    assert _plugin_results('def f():\n    print(0)\n    print(0)') == tuple(
        _out(line, column=5) for line in (2, 3)
    )
