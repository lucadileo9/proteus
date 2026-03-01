"""
Writer layer — Template Method pattern.

BaseWriter defines the fixed writing algorithm.
Concrete writers implement only ``_serialize()``,
delegating the actual serialization logic to their Adapter.
"""

from .base import BaseWriter
from .json_writer import JSONWriter
from .yaml_writer import YAMLWriter
from .env_writer import EnvWriter

__all__ = [
    "BaseWriter",
    "JSONWriter",
    "YAMLWriter",
    "EnvWriter",
]
