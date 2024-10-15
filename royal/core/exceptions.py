class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)
        self.message = extra
        self.extra = extra or {}