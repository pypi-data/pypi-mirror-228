"""
Validation functions.
"""

import os
import re

import src.exceptions as exceptions

def is_valid_name(name: str):
    """
    Validate project and module names.
    """
    return re.match(r'^\w+$', name) is not None


def check_project_name(name: str):
    """
    Check if the project name is valid.
    """
    if not is_valid_name(name):
        raise exceptions.InvalidNameProjectException()

    if os.path.exists(name):
        raise exceptions.ProjectAlreadyExistsException()

def check_module_name(name: str):
    """
    Check if the module name is valid.
    """
    if name and not is_valid_name(name):
        raise exceptions.InvalidNameModuleException(name)

def check_module_names(names: list[str]):
    """
    Check if the module names are valid.
    """
    for name in names:
        check_module_name(name)
