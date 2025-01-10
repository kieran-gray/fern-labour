from pathlib import Path
from typing import Any

from jinja2 import Template


class Jinja2EmailGenerationService:
    def __init__(self) -> None:
        self.directory = Path(__file__).parent / "templates" / "build"

    def generate(self, template_name: str, data: dict[str, Any]) -> str:
        """
        Generate a html string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        template_str = self.directory.joinpath(template_name).read_text()
        html_content = Template(template_str).render(data)
        return html_content
