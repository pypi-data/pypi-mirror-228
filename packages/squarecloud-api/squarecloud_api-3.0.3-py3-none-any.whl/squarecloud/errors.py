class SquareException(BaseException):
    """abstract class SquareException"""


class RequestError(SquareException):
    """raised when a request fails"""


class AuthenticationFailure(RequestError):
    """raised when an API token is invalid"""


class NotFoundError(RequestError):
    """raises when a request returns a 404 response"""


class BadRequestError(RequestError):
    """raises when a request returns a 400 response"""


class ApplicationNotFound(SquareException):
    """raises when an application is not found"""


class InvalidFile(SquareException):
    """raised when a file is invalid"""


class MissingConfigFile(RequestError):
    """raised when the configuration file is missing"""


class MissingDependenciesFile(RequestError):
    """raised when the configuration file is missing"""
