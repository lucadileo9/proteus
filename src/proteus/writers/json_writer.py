"""
Concrete writer for JSON files.

Delegates serialization to ``JSONAdapter`` — contains no direct ``json`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from .base import BaseWriter
from ..adapters.json_adapter import JSONAdapter


class JSONWriter(BaseWriter):
    """
    JSON writer — Template Method concrete participant.

    Implements ``_serialize()`` by delegating to the JSONAdapter.
    All JSON-specific serialization logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or JSONAdapter()

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate to JSONAdapter.dump()."""
        return self._adapter.dump(data)
