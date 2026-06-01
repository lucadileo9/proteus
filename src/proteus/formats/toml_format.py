from typing import List

from ..adapters.toml_adapter import TOMLAdapter
from ..readers.toml_reader import TOMLReader
from ..writers.toml_writer import TOMLWriter
from .base_format import FormatCreator


class TOMLFormatCreator(FormatCreator):
    """
    Creator factory for TOML readers and writers.
    """

    def __init__(self) -> None:
        """Initialize the TOMLFormatCreator with a shared adapter."""
        self._adapter = TOMLAdapter()

    def create_reader(self) -> TOMLReader:
        """Create a TOMLReader instance sharing the adapter."""
        return TOMLReader(adapter=self._adapter)

    def create_writer(self) -> TOMLWriter:
        """Create a TOMLWriter instance sharing the adapter."""
        return TOMLWriter(adapter=self._adapter)

    def get_extensions(self) -> List[str]:
        """Return the supported file extensions for TOML."""
        return [".toml"]
