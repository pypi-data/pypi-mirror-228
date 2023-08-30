from __future__ import annotations

import shlex
import subprocess
from collections.abc import Sequence
from typing import Protocol

import attrs


class DiffPrinter(Protocol):
    def print(self, diff_lines: Sequence[str]) -> None: ...


class StdOutPrinter:
    def print(self, diff_lines: Sequence[str]) -> None:
        print(*diff_lines, sep='', end='')


@attrs.frozen
class PagerPrinter:
    pager: str

    def print(self, diff_lines: Sequence[str]) -> None:
        subprocess.run(shlex.split(self.pager), input=''.join(diff_lines), text=True)
