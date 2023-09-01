"""
Module-specific custom exceptions
"""

import src.constants as constants


class InvalidNameProjectException(Exception):
    """
    Exception raised when the name of the project is invalid
    """
    def __init__(self, message=constants.INVALID_NAME_PROJECT):
        super().__init__(message)

class ProjectAlreadyExistsException(Exception):
    """
    Exception raised when the project already exists
    """
    def __init__(self, message=constants.PROJECT_ALREADY_EXISTS):
        super().__init__(message)

class InvalidNameModuleException(Exception):
    """
    Exception raised when the name of a module is invalid
    """
    def __init__(self, module, message=constants.INVALID_NAME_MODULE):
        super().__init__(message.format(module=module))
