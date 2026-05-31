"""
Concrete reader for .env files.

Delegates parsing to ``EnvAdapter`` — contains no direct ``dotenv`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from ..adapters.env_adapter import EnvAdapter
from .base import BaseReader


class EnvReader(BaseReader):
    """
    .env reader — Template Method concrete participant.

    Implements ``_parse_content()`` by delegating to the EnvAdapter.
    All .env-specific parsing logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or EnvAdapter()

    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """Delegate to EnvAdapter.load()."""
        return self._adapter.load(raw)
