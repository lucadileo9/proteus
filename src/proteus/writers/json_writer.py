"""
Concrete writer for JSON files.

Delegates serialization to ``JSONAdapter`` — contains no direct ``json`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.json_adapter import JSONAdapter
from .generic import GenericWriter


class JSONWriter(GenericWriter):
    """
    Concrete writer for JSON files.

    Inherits delegation logic from ``GenericWriter``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the JSONWriter.

        Args:
            adapter: Optional custom adapter. Defaults to ``JSONAdapter``.
        """
        super().__init__(adapter=adapter or JSONAdapter())
