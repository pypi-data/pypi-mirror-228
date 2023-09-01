"""
Automatically generate a hexagonal architecture project structure in Python.
Easily customizable to include user-defined modules.
"""

from src.utils.input import get_project_name, get_module_names
from src.utils.structure import add_modules_to_base_structure, create_structure
from src.utils.structure_loader import load_structure_from_json
from src.constants import BASE_STRUCTURE_JSON


def main():
    """
    Main function for the script.
    """
    # Prompt for project name and module names
    project_name: str = get_project_name()
    module_names: list[str] = get_module_names()

    # Hexagonal modular architecture
    hexagonal_structure: dict = {
        project_name: load_structure_from_json(BASE_STRUCTURE_JSON),
    }

    # Add generic modules with descriptions as an example
    add_modules_to_base_structure(hexagonal_structure[project_name], module_names)

    # Create the folder and file structure
    create_structure(hexagonal_structure)


if __name__ == "__main__":
    main()
