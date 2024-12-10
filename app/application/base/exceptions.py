class ApplicationError(Exception):
    pass


class AdapterError(ApplicationError):
    pass


class GatewayError(ApplicationError):
    pass
