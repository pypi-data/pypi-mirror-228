"""
This module contains the structure loader.
"""

import json


def load_structure_from_json(file_path: str) -> dict:
    """
    Load the structure from a JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as _f:
        return json.load(_f)
