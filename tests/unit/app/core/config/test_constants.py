from pathlib import Path

from app.core.constants import BASE_DIR


def test_base_dir():
    expected = Path(__file__).parent.parent.parent.parent.parent.parent
    assert expected == BASE_DIR
