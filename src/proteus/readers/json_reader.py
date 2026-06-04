"""
Concrete reader for JSON files.

Delegates parsing to ``JSONAdapter`` — contains no direct ``json`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.json_adapter import JSONAdapter
from .generic import GenericReader


class JSONReader(GenericReader):
    """
    Concrete reader for JSON files.

    Inherits delegation logic from ``GenericReader``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the JSONReader.

        Args:
            adapter: Optional custom adapter. Defaults to ``JSONAdapter``.
        """
        super().__init__(adapter=adapter or JSONAdapter())
