"""
This module contains the structure loader.
"""

import json
from pkg_resources import resource_filename

from src.constants import TEMPLATE_PATH, SRC_PATH


def load_structure_from_json(file_name: str) -> dict:
    """
    Load the structure from a JSON file.
    """
    file_path = resource_filename(SRC_PATH, TEMPLATE_PATH.format(template=file_name))
    with open(file_path, 'r', encoding='utf-8') as _f:
        return json.load(_f)
