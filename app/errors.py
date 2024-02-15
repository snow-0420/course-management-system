class InstanceExistError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InstanceNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
