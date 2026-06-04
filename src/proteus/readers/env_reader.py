"""
Concrete reader for .env files.

Delegates parsing to ``EnvAdapter`` — contains no direct ``dotenv`` usage.
"""

from typing import Optional

from ..adapters.base import BaseAdapter
from ..adapters.env_adapter import EnvAdapter
from .generic import GenericReader


class EnvReader(GenericReader):
    """
    Concrete reader for .env files.

    Inherits delegation logic from ``GenericReader``.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        """
        Initialize the EnvReader.

        Args:
            adapter: Optional custom adapter. Defaults to ``EnvAdapter``.
        """
        super().__init__(adapter=adapter or EnvAdapter())
