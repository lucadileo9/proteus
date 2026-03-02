"""
Factory Method pattern (GoF canonical) — abstract creator.

``FormatCreator`` declares the two factory methods that every
concrete creator must implement:

    - ``create_reader()`` → returns a ``BaseReader`` for the format
    - ``create_writer()`` → returns a ``BaseWriter`` for the format

Each concrete creator couples reader and writer of the **same** format,
guaranteeing internal coherence.  The ``ConfigurationManager`` depends
only on ``FormatCreator`` — never on concrete reader/writer classes
(Dependency Inversion Principle).
"""

from abc import ABC, abstractmethod
from typing import List

from ..readers.base import BaseReader
from ..writers.base import BaseWriter


class FormatCreator(ABC):
    """
    Factory Method (GoF) — Abstract Creator.

    Subclasses implement the two factory methods to return a
    format-specific reader/writer pair.  ``get_extensions()``
    advertises which file extensions the creator handles so the
    manager can dispatch automatically.

    """

    @abstractmethod
    def create_reader(self) -> BaseReader:
        """Factory Method — create the reader for this format."""

    @abstractmethod
    def create_writer(self) -> BaseWriter:
        """Factory Method — create the writer for this format."""

    @abstractmethod
    def get_extensions(self) -> List[str]:
        """Return file extensions handled by this creator (e.g. ``['.json']``)."""
