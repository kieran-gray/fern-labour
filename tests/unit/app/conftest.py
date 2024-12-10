import pytest

from app.core.settings import Settings
from tests.unit.app.core.config.conftest import MockConfigReader


@pytest.fixture
def mock_settings(mock_config_reader: MockConfigReader) -> Settings:
    return Settings.from_file(reader=mock_config_reader)
