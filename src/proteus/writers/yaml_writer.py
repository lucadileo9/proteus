"""
Concrete writer for YAML files.

Delegates serialization to ``YAMLAdapter`` — contains no direct ``yaml`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.yaml_adapter import YAMLAdapter
from .generic import GenericWriter


class YAMLWriter(GenericWriter):
    """
    Concrete writer for YAML files.

    Inherits delegation logic from ``GenericWriter``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the YAMLWriter.

        Args:
            adapter: Optional custom adapter. Defaults to ``YAMLAdapter``.
        """
        super().__init__(adapter=adapter or YAMLAdapter())
