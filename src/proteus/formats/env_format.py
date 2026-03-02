"""
Factory Method (GoF) — Concrete Creator for ENV (.env) format.

Couples ``EnvReader`` and ``EnvWriter``, both backed by the same
``EnvAdapter``, ensuring full format coherence.
"""

from typing import List

from .base_format import FormatCreator
from ..readers.env_reader import EnvReader
from ..writers.env_writer import EnvWriter


class EnvFormatCreator(FormatCreator):
    """
    Concrete Creator — ENV.

    Creates the reader/writer pair for ``.env`` files.
    Handles the ``.env`` extension.
    """

    def create_reader(self) -> EnvReader:
        """Return a new ``EnvReader`` instance."""
        return EnvReader()

    def create_writer(self) -> EnvWriter:
        """Return a new ``EnvWriter`` instance."""
        return EnvWriter()

    def get_extensions(self) -> List[str]:
        """ENV uses a single extension."""
        return [".env"]
