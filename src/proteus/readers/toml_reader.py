"""
Concrete reader for TOML files.

Delegates parsing to ``TOMLAdapter`` — contains no direct ``toml`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.toml_adapter import TOMLAdapter
from .generic import GenericReader


class TOMLReader(GenericReader):
    """
    Concrete reader for TOML files.

    Inherits delegation logic from ``GenericReader``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the TOMLReader.

        Args:
            adapter: Optional custom adapter. Defaults to ``TOMLAdapter``.
        """
        super().__init__(adapter=adapter or TOMLAdapter())
