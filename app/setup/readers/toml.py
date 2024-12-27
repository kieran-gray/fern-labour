import os
from pathlib import Path
from typing import Any

import rtoml

from app.setup.readers.abstract import ConfigReader


class TomlConfigReader(ConfigReader):
    def read(self, path: Path, override: bool = True) -> dict[str, Any]:
        with open(path, encoding="utf-8") as f:
            toml = rtoml.load(f)
        return self.override(toml) if override else toml

    def override(self, toml: dict[str, Any]) -> dict[str, Any]:
        """Override any values in the config.toml that are set in the environment."""
        for key, value in toml.items():
            if isinstance(value, dict):
                self.override(value)
            if value := os.getenv(key):
                toml[key] = value
        return toml
