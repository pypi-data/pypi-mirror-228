from __future__ import annotations

import difflib
from typing import Protocol

import attrs

from ..config import TemplateConfig
from ..printers import DiffPrinter
from ..rendering import TemplateRenderer


class Reader(Protocol):
    def read_lines(self, file_path: str) -> list[str]: ...


@attrs.frozen
class Differ:
    reader: Reader
    renderer: TemplateRenderer
    printer: DiffPrinter

    def print_diff(self, templates: TemplateConfig) -> None:
        for file in templates.files:
            current_lines = self.reader.read_lines(file.destination_path)

            rendered_lines = (
                self.renderer.render(file.template_name).splitlines(keepends=True)
            )

            diff_lines = list(
                difflib.unified_diff(
                    current_lines, rendered_lines,
                    fromfile=file.destination_path,
                    tofile=file.destination_path,
                ),
            )

            if not diff_lines:
                continue

            self.printer.print(diff_lines)
