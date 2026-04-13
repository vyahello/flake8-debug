from abc import ABC
from typing import Final


class Error(ABC):
    code: str
    func_name: str

    @property
    def msg(self) -> str:
        return f'{self.code} {self.func_name}() function usage is detected'


class PrintError(Error):
    code: str = 'DB100'
    func_name: str = 'print'


class BreakpointError(Error):
    code: str = 'DB200'
    func_name: str = 'breakpoint'


class BreakpointHookError(Error):
    code: str = 'DB201'
    func_name: str = 'breakpointhook'


class PdbError(Error):
    code: str = 'DB300'
    func_name: str = 'set_trace'


ERRORS: Final[tuple[type[Error], ...]] = (
    PrintError,
    BreakpointError,
    BreakpointHookError,
    PdbError,
)
