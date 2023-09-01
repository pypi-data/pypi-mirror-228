class InvalidCredentialsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class NotFoundError(Exception):
    pass


class TooManyRequestsError(Exception):
    pass


class UnknownError(Exception):
    pass
