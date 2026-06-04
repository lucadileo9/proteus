"""
Concrete reader for YAML files.

Delegates parsing to ``YAMLAdapter`` — contains no direct ``yaml`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.yaml_adapter import YAMLAdapter
from .generic import GenericReader


class YAMLReader(GenericReader):
    """
    Concrete reader for YAML files.

    Inherits delegation logic from ``GenericReader``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the YAMLReader.

        Args:
            adapter: Optional custom adapter. Defaults to ``YAMLAdapter``.
        """
        super().__init__(adapter=adapter or YAMLAdapter())
