from pathlib import Path
from typing import Any, Protocol


class ConfigReader(Protocol):
    def read(self, path: Path) -> dict[str, Any]: ...
