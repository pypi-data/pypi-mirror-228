class CoralException(Exception):
    pass


class NotFound(CoralException):
    pass


class ConfigError(CoralException):
    pass
