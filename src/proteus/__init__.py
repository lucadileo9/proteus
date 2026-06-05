"""
Proteus — Unified configuration management and translation library.

Design patterns implemented:
    - **Optional Singleton**: ``ConfigurationManager.instance()``
      (shared global instance when needed)
    - **Facade**:          ``ConfigurationManager`` (simplified public API)
    - **Factory Method**:  ``FormatCreator`` (reader/writer pair creation)
    - **Template Method**: ``BaseReader`` / ``BaseWriter`` (fixed algorithms)
    - **Adapter**:         ``BaseAdapter`` (wraps external libraries)

Quick start::

    from proteus import ConfigurationManager

    config = ConfigurationManager()
    config.load("settings.yaml")
    print(config.get("database.host"))
    config.translate("settings.yaml", "settings.json")
    with ConfigurationManager.temporary() as temp:
        temp.load("settings.yaml")
"""

from .adapters.base import BaseAdapter
from .core import ConfigurationManager
from .exceptions import (
    ConfigurationError,
    ConfigurationNotLoadedError,
    ConfigurationTypeError,
    InvalidKeyError,
    UnsupportedFormatError,
)
from .formats.base_format import FormatCreator
from .formats.generic import GenericFormatCreator
from .readers.base import BaseReader
from .writers.base import BaseWriter

__version__ = "0.2.0"

Proteus = ConfigurationManager  # Alias per chi preferisce un'API più compatta

__all__ = [
    "ConfigurationManager",
    "Proteus",
    "FormatCreator",
    "GenericFormatCreator",
    "BaseReader",
    "BaseWriter",
    "BaseAdapter",
    "ConfigurationError",
    "UnsupportedFormatError",
    "InvalidKeyError",
    "ConfigurationNotLoadedError",
    "ConfigurationTypeError",
]
