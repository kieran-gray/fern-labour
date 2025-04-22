import pytest

from src.common.application.exceptions import ApplicationError


def test_raise_application_error():
    """For the coverage"""
    with pytest.raises(ApplicationError):
        raise ApplicationError()
