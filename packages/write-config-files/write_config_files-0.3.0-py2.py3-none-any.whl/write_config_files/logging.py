from __future__ import annotations

import sys
from typing import Protocol


class Logger(Protocol):
    def debug(self, msg: str) -> None: ...
    def info(self, msg: str) -> None: ...
    def warn(self, msg: str) -> None: ...


class StdErrLogger:
    def debug(self, msg: str) -> None:
        print(msg, file=sys.stderr)

    def info(self, msg: str) -> None:
        print(msg, file=sys.stderr)

    def warn(self, msg: str) -> None:
        print(msg, file=sys.stderr)


class StdErrColorLogger:
    def debug(self, msg: str) -> None:
        print(f'\033[2m{msg}\033[0m', file=sys.stderr)

    def info(self, msg: str) -> None:
        print(f'\033[0m{msg}\033[0m', file=sys.stderr)

    def warn(self, msg: str) -> None:
        print(f'\033[93m{msg}\033[0m', file=sys.stderr)
