"""
Concrete writer for .env files.

Delegates serialization to ``EnvAdapter`` — contains no direct ``dotenv`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.env_adapter import EnvAdapter
from .generic import GenericWriter


class EnvWriter(GenericWriter):
    """
    Concrete writer for .env files.

    Inherits delegation logic from ``GenericWriter``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the EnvWriter.

        Args:
            adapter: Optional custom adapter. Defaults to ``EnvAdapter``.
        """
        super().__init__(adapter=adapter or EnvAdapter())
