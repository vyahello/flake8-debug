from abc import ABC
from typing import ClassVar, Final


class Error(ABC):
    code: ClassVar[str]
    func_name: ClassVar[str]

    @property
    def msg(self) -> str:
        return f'{self.code} {self.func_name}() function usage is detected'


class PrintError(Error):
    code: ClassVar[str] = 'DB100'
    func_name: ClassVar[str] = 'print'


class BreakpointError(Error):
    code: ClassVar[str] = 'DB200'
    func_name: ClassVar[str] = 'breakpoint'


class BreakpointHookError(Error):
    code: ClassVar[str] = 'DB201'
    func_name: ClassVar[str] = 'breakpointhook'


class PdbError(Error):
    code: ClassVar[str] = 'DB300'
    func_name: ClassVar[str] = 'set_trace'


ERRORS: Final[tuple[type[Error], ...]] = (
    PrintError,
    BreakpointError,
    BreakpointHookError,
    PdbError,
)
