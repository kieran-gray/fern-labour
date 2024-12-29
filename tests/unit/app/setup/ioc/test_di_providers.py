from dishka import make_async_container

from app.setup.ioc.ioc_registry import get_providers


def test_can_create_dishka_container():
    make_async_container(*get_providers())
