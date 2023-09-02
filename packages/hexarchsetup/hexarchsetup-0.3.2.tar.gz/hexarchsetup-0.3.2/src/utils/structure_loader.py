"""
This module contains the structure loader.
"""

import json
from importlib.resources import read_text

from src.constants import TEMPLATES_MODULE


def load_structure_from_json(file_name: str) -> dict:
    """
    Load the structure from a JSON file.
    """
    return json.loads(read_text(TEMPLATES_MODULE, file_name))
