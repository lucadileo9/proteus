"""
Concrete writer for .env files.

Delegates serialization to ``EnvAdapter`` — contains no direct ``dotenv`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from ..adapters.env_adapter import EnvAdapter
from .base import BaseWriter


class EnvWriter(BaseWriter):
    """
    .env writer — Template Method concrete participant.

    Implements ``_serialize()`` by delegating to the EnvAdapter.
    All .env-specific serialization logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or EnvAdapter()

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate to EnvAdapter.dump()."""
        return self._adapter.dump(data)
