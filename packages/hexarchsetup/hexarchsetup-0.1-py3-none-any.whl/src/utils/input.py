"""
This module contains functions to get input from the user.
"""

from src.utils.validation import check_project_name, check_module_names

def get_project_name():
    """
    Get the project name from the user.
    """
    project_name: str = input("Enter the project name: ").strip()
    check_project_name(project_name)
    return project_name


def get_module_names():
    """
    Get the module names from the user.
    """
    module_names_input: str = input("Enter module names separated by commas: ")
    module_names: list[str] = "".join(module_names_input.split()).split(',')
    check_module_names(module_names)
    return module_names
