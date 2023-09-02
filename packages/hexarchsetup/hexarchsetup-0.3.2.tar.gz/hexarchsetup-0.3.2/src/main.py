"""
Automatically generate a hexagonal architecture project structure in Python.
Easily customizable to include user-defined modules.
"""

from copy import deepcopy

from src.utils.input import get_project_name, get_module_names
from src.utils.structure import add_modules_to_root_structure, create_structure, migrate_to_test_structure
from src.utils.structure_loader import load_structure_from_json
from src.constants import BASE_STRUCTURE_JSON, ROOT_STRUCTURE_JSON, SOURCE_PATH, TESTS_PATH


def main():
    """
    Main function for the script.
    """
    # Prompt for project name and module names
    project_name: str = get_project_name()
    module_names: list[str] = get_module_names()

    # Load the root structure
    root_structure: dict = load_structure_from_json(ROOT_STRUCTURE_JSON)

    # Load the base structure
    base_structure: dict = load_structure_from_json(BASE_STRUCTURE_JSON)
    test_base_structure: dict = migrate_to_test_structure(deepcopy(base_structure))

    # Add the base structure to the root structure
    root_structure[SOURCE_PATH] = base_structure
    root_structure[TESTS_PATH] = test_base_structure

    # Add the module names to the structure
    add_modules_to_root_structure(root_structure, module_names)

    # Hexagonal modular architecture
    hexagonal_structure: dict = {
        project_name: root_structure,
    }

    # Create the folder and file structure
    create_structure(hexagonal_structure)


if __name__ == "__main__":
    main()
