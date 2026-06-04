"""
Concrete writer for TOML files.

Delegates serialization to ``TOMLAdapter`` — contains no direct ``toml`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.toml_adapter import TOMLAdapter
from .generic import GenericWriter


class TOMLWriter(GenericWriter):
    """
    Concrete writer for TOML files.

    Inherits delegation logic from ``GenericWriter``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the TOMLWriter.

        Args:
            adapter: Optional custom adapter. Defaults to ``TOMLAdapter``.
        """
        super().__init__(adapter=adapter or TOMLAdapter())
