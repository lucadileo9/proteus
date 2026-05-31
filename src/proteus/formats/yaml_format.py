"""
Factory Method (GoF) — Concrete Creator for YAML format.

Couples ``YAMLReader`` and ``YAMLWriter``, both backed by the same
``YAMLAdapter``, ensuring full format coherence.
"""

from typing import List

from ..adapters.yaml_adapter import YAMLAdapter
from ..readers.yaml_reader import YAMLReader
from ..writers.yaml_writer import YAMLWriter
from .base_format import FormatCreator


class YAMLFormatCreator(FormatCreator):
    """
    Concrete Creator — YAML.

    Creates the reader/writer pair for YAML files.
    Handles both ``.yaml`` and ``.yml`` extensions.
    """

    def __init__(self) -> None:
        self._adapter = YAMLAdapter()

    def create_reader(self) -> YAMLReader:
        """Return a new ``YAMLReader`` instance."""
        return YAMLReader(adapter=self._adapter)

    def create_writer(self) -> YAMLWriter:
        """Return a new ``YAMLWriter`` instance."""
        return YAMLWriter(adapter=self._adapter)

    def get_extensions(self) -> List[str]:
        """YAML allows two common extensions."""
        return [".yaml", ".yml"]
