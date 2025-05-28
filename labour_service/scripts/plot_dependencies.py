import dishka.plotter
import uvloop
from dishka import AsyncContainer, make_async_container

from src.setup.settings import Settings
from src.setup.ioc.ioc_registry import get_providers


def make_plot_data_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})


def generate_dependency_graph_d2(container: AsyncContainer) -> str:
    """
    Generates a dependency graph for the container in `d2` format.
    See https://d2lang.com for rendering instructions.
    """
    return dishka.plotter.render_d2(container)


def generate_dependency_graph_mermaid(container: AsyncContainer) -> str:
    """
    Generates a dependency graph for the container in `d2` format.
    See https://d2lang.com for rendering instructions.
    """
    return dishka.plotter.render_mermaid(container)


async def main():
    settings: Settings = Settings.from_file()
    container = make_plot_data_container(settings)
    print(generate_dependency_graph_d2(container))


if __name__ == "__main__":
    uvloop.run(main())
