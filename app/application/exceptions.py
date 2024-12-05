from app.application.base.exceptions import ApplicationError


class AdapterError(ApplicationError):
    pass


class GatewayError(ApplicationError):
    pass
