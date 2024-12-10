from pathlib import Path
from typing import Any

import rtoml

from app.core.readers.abstract import ConfigReader


class TomlConfigReader(ConfigReader):
    def read(self, path: Path) -> dict[str, Any]:
        with open(path, encoding="utf-8") as f:
            return rtoml.load(f)
