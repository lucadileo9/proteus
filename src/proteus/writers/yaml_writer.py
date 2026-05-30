"""
Concrete writer for YAML files.

Delegates serialization to ``YAMLAdapter`` — contains no direct ``yaml`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from .base import BaseWriter
from ..adapters.yaml_adapter import YAMLAdapter


class YAMLWriter(BaseWriter):
    """
    YAML writer — Template Method concrete participant.

    Implements ``_serialize()`` by delegating to the YAMLAdapter.
    All YAML-specific serialization logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or YAMLAdapter()

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate to YAMLAdapter.dump()."""
        return self._adapter.dump(data)
