"""
Concrete reader for YAML files.

Delegates parsing to ``YAMLAdapter`` — contains no direct ``yaml`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from ..adapters.yaml_adapter import YAMLAdapter
from .base import BaseReader


class YAMLReader(BaseReader):
    """
    YAML reader — Template Method concrete participant.

    Implements ``_parse_content()`` by delegating to the YAMLAdapter.
    All YAML-specific parsing logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or YAMLAdapter()

    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """Delegate to YAMLAdapter.load()."""
        return self._adapter.load(raw)
