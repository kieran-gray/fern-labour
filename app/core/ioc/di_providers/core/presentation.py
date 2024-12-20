from dishka import Provider, Scope, from_context
from starlette.requests import Request


class PresentationProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)
