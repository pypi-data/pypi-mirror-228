from __future__ import annotations

from typing import Protocol

import attrs

from ..config import TemplateConfig
from ..logging import Logger
from ..rendering import TemplateRenderer


class FileSystem(Protocol):
    def file_exists(self, path: str) -> bool: ...
    def read_content(self, path: str) -> str: ...
    def write_file(self, path: str, content: str, is_executable: bool) -> None: ...


@attrs.frozen
class Writer:
    renderer: TemplateRenderer
    file_system: FileSystem
    logger: Logger

    def write(self, templates: TemplateConfig, skip_if_exists: bool) -> None:
        for file in templates.files:
            rendered_content = self.renderer.render(file.template_name)

            already_exists = self.file_system.file_exists(file.destination_path)
            current_content = self.file_system.read_content(file.destination_path)

            if not already_exists:
                self.logger.info(f'writing {file.destination_path}')
            elif skip_if_exists:
                self.logger.debug(
                    f'skipping {file.destination_path} because it already exists',
                )
                continue
            elif rendered_content == current_content:
                self.logger.debug(
                    f'skipping {file.destination_path} because there are no changes',
                )
                continue
            else:
                self.logger.warn(f'overwriting {file.destination_path}')

            self.file_system.write_file(
                file.destination_path,
                rendered_content,
                file.is_executable,
            )
