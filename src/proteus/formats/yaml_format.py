"""
Factory Method (GoF) — Concrete Creator for YAML format.

Couples ``YAMLReader`` and ``YAMLWriter``, both backed by the same
``YAMLAdapter``, ensuring full format coherence.
"""

from typing import List

from .base_format import FormatCreator
from ..readers.yaml_reader import YAMLReader
from ..writers.yaml_writer import YAMLWriter


class YAMLFormatCreator(FormatCreator):
    """
    Concrete Creator — YAML.

    Creates the reader/writer pair for YAML files.
    Handles both ``.yaml`` and ``.yml`` extensions.
    """

    def create_reader(self) -> YAMLReader:
        """Return a new ``YAMLReader`` instance."""
        return YAMLReader()

    def create_writer(self) -> YAMLWriter:
        """Return a new ``YAMLWriter`` instance."""
        return YAMLWriter()

    def get_extensions(self) -> List[str]:
        """YAML allows two common extensions."""
        return [".yaml", ".yml"]
