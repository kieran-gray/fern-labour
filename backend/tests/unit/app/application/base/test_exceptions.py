import pytest

from app.application.base.exceptions import ApplicationError


def test_raise_application_error():
    """For the coverage"""
    with pytest.raises(ApplicationError):
        raise ApplicationError()
