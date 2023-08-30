from __future__ import annotations

import os.path
from typing import Any
from typing import Protocol

import attrs
import yaml


@attrs.frozen
class TemplateFile:
    template_name: str
    """Name of the template for this file."""

    destination_path: str
    """Path the file should be written to."""

    is_executable: bool
    """Whether this file should be made executable."""


@attrs.frozen
class TemplateConfig:
    root_dir: str
    """The root directory for all templates.

    All template paths are relative to this directory.
    """

    files: tuple[TemplateFile, ...]
    """The templates that should be rendered."""


class ConfigParser(Protocol):
    def parse_template_config(self, file_content: str) -> TemplateConfig: ...
    def parse_context(self, file_content: str) -> dict[str, Any]: ...


class YamlParser:
    def parse_template_config(self, file_content: str) -> TemplateConfig:
        data = yaml.safe_load(file_content)

        files = []
        for group in data['config_files']:
            output_dir = os.path.expanduser(group['output_dir'])
            for template in group['templates']:
                template_name = template['template']
                destination = template.get('destination')
                if destination is not None:
                    destination = os.path.join(output_dir, destination)
                else:
                    destination = os.path.join(output_dir, template_name)

                files.append(
                    TemplateFile(
                        template_name=template_name,
                        destination_path=destination,
                        is_executable=template.get('is_executable', False),
                    ),
                )

        return TemplateConfig(
            root_dir=data['root_template_dir'],
            files=tuple(files),
        )

    def parse_context(self, file_content: str) -> dict[str, Any]:
        return yaml.safe_load(file_content)
