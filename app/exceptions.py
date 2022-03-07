class BaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()


class AppException(BaseException):
    def __init__(self, message):
        super().__init__(message)


class ValidationException(BaseException):
    def __init__(self, message):
        super().__init__(message)
