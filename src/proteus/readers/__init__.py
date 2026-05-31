"""
Reader layer — Template Method pattern.

BaseReader defines the fixed parsing algorithm.
Concrete readers implement only ``_parse_content()``,
delegating the actual parsing logic to their Adapter.
"""

from .base import BaseReader
from .env_reader import EnvReader
from .json_reader import JSONReader
from .yaml_reader import YAMLReader

__all__ = [
    "BaseReader",
    "JSONReader",
    "YAMLReader",
    "EnvReader",
]
