from pathlib import Path

from src.setup.constants import BASE_DIR


def test_base_dir():
    expected = Path(__file__).parent.parent.parent.parent.parent.parent
    assert expected == BASE_DIR
