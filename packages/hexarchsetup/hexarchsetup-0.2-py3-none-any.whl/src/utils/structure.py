"""
This module contains the functions for creating the folder and file structure.
"""

import os

from src.utils.structure_loader import load_structure_from_json
from src.constants import MODULE_STRUCTURE_JSON, MODULE_NAME_REPLACEMENT, DESCRIPTION_FORMAT


def create_structure(structure: dict, parent_folder: str = ""):
    """
    Creates the folder and file structure based on the given dictionary.
    """
    for key, value in structure.items():
        if isinstance(value, dict):
            new_folder = os.path.join(parent_folder, key)
            os.makedirs(new_folder, exist_ok=True)
            create_structure(value, new_folder)
        else:
            new_file = os.path.join(parent_folder, key)
            with open(new_file, "w", encoding="utf-8") as _f:
                description = DESCRIPTION_FORMAT.format(value=value) if value else ""
                _f.write(description)


def add_module_to_base_structure(base_structure: dict, module_structure: dict, module_name: str):
    """
    Add the module to the base structure.
    """
    for key, value in module_structure.items():
        if isinstance(value, dict):
            add_module_to_base_structure(
                base_structure.setdefault(key.replace(MODULE_NAME_REPLACEMENT, module_name), {}),
                value,
                module_name,
            )
        else:
            formatted_key = key.replace(MODULE_NAME_REPLACEMENT, module_name)
            base_structure[formatted_key] = value


def add_modules_to_base_structure(structure: dict, module_names: list[str]):
    """
    Add the module names to the structure.
    """
    module_structure = load_structure_from_json(MODULE_STRUCTURE_JSON)
    for module_name in module_names:
        add_module_to_base_structure(structure, module_structure, module_name)
