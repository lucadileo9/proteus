"""
Factory Method (GoF) — Concrete Creator for JSON format.

Couples ``JSONReader`` and ``JSONWriter``, both backed by the same
``JSONAdapter``, ensuring full format coherence.
"""

from typing import List

from ..adapters.json_adapter import JSONAdapter
from .base_format import FormatCreator
from ..readers.json_reader import JSONReader
from ..writers.json_writer import JSONWriter


class JSONFormatCreator(FormatCreator):
    """
    Concrete Creator — JSON.

    Creates the reader/writer pair for JSON files.
    Handles the ``.json`` extension.
    """

    def __init__(self) -> None:
        self._adapter = JSONAdapter()

    def create_reader(self) -> JSONReader:
        """Return a new ``JSONReader`` instance."""
        return JSONReader(adapter=self._adapter)

    def create_writer(self) -> JSONWriter:
        """Return a new ``JSONWriter`` instance."""
        return JSONWriter(adapter=self._adapter)

    def get_extensions(self) -> List[str]:
        """JSON uses a single extension."""
        return [".json"]
