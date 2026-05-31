"""
Concrete writer for TOML files.

Delegates serialization to ``TOMLAdapter`` — contains no direct ``toml`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from ..adapters.toml_adapter import TOMLAdapter
from .base import BaseWriter


class TOMLWriter(BaseWriter):
    """
    TOML writer — Template Method concrete participant.

    Implements ``_serialize()`` by delegating to the TOMLAdapter.
    All TOML-specific serialization logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or TOMLAdapter()

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate to TOMLAdapter.dump()."""
        return self._adapter.dump(data)
