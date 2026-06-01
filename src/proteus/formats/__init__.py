"""
Format Creator layer — Factory Method pattern (GoF canonical).

Each concrete ``FormatCreator`` couples a reader and a writer for the
same configuration format.  The ``ConfigurationManager`` depends only
on the abstract ``FormatCreator`` interface, never on concrete
readers or writers (Dependency Inversion Principle).
"""

from .base_format import FormatCreator
from .env_format import EnvFormatCreator
from .json_format import JSONFormatCreator
from .toml_format import TOMLFormatCreator
from .yaml_format import YAMLFormatCreator

__all__ = [
    "FormatCreator",
    "JSONFormatCreator",
    "YAMLFormatCreator",
    "TOMLFormatCreator",
    "EnvFormatCreator",
]
