from __future__ import annotations

from typing import Any
from typing import Protocol

import attrs
import jinja2


class TemplateRenderer(Protocol):
    def render(self, template_name: str) -> str: ...


@attrs.frozen
class Jinja2Renderer:
    loader: jinja2.BaseLoader
    context: dict[str, Any]

    env: jinja2.Environment = attrs.field(init=False)

    @env.default
    def _env(self) -> jinja2.Environment:
        return jinja2.Environment(
            loader=self.loader,
            autoescape=jinja2.select_autoescape(),
            keep_trailing_newline=True,
            lstrip_blocks=True,
            trim_blocks=True,
        )

    def render(self, template_name: str) -> str:
        template = self.env.get_template(template_name)
        return template.render(**self.context)
