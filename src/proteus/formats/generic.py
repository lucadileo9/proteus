from typing import TYPE_CHECKING, List

from ..readers.generic import GenericReader
from ..writers.generic import GenericWriter
from .base_format import FormatCreator

if TYPE_CHECKING:
    from ..adapters.base import BaseAdapter


class GenericFormatCreator(FormatCreator):
    """
    Standard "bridge" creator that couples an adapter with generic reader/writer.

    This allows adding new formats by providing only a BaseAdapter implementation.
    """

    def __init__(self, extensions: List[str], adapter: "BaseAdapter") -> None:
        """
        Initialize the generic creator.

        Args:
            extensions: List of file extensions (e.g. ``['.ini']``).
            adapter: The concrete adapter to use for this format.
        """
        self._extensions = extensions
        self._adapter = adapter

    def create_reader(self) -> GenericReader:
        """Return a GenericReader using the shared adapter."""
        return GenericReader(self._adapter)

    def create_writer(self) -> GenericWriter:
        """Return a GenericWriter using the shared adapter."""
        return GenericWriter(self._adapter)

    def get_extensions(self) -> List[str]:
        """Return the user-defined extensions."""
        return self._extensions
