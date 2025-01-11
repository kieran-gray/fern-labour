from pathlib import Path
from typing import Any, Protocol


class EmailGenerationService(Protocol):
    """Abstract Base Class for an email generation service."""

    directory: Path

    def generate(self, template_name: str, data: dict[str, Any]) -> str:
        """
        Generate a html string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
