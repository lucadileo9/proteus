"""
Concrete writer for .env files.

Delegates serialization to ``EnvAdapter`` — contains no direct ``dotenv`` usage.
"""

from typing import Any, Dict

from .base import BaseWriter
from ..adapters.env_adapter import EnvAdapter


class EnvWriter(BaseWriter):
    """
    .env writer — Template Method concrete participant.

    Implements ``_serialize()`` by delegating to the EnvAdapter.
    All .env-specific serialization logic lives in the adapter, not here.
    """

    def __init__(self) -> None:
        self._adapter = EnvAdapter()

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate to EnvAdapter.dump()."""
        return self._adapter.dump(data)
