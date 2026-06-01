"""
Concrete reader for TOML files.

Delegates parsing to ``TOMLAdapter`` — contains no direct ``toml`` usage.
"""

from typing import Any, Dict, Optional

from ..adapters.base import BaseAdapter
from ..adapters.toml_adapter import TOMLAdapter
from .base import BaseReader


class TOMLReader(BaseReader):
    """
    TOML reader — Template Method concrete participant.

    Implements ``_parse_content()`` by delegating to the TOMLAdapter.
    All TOML-specific parsing logic lives in the adapter, not here.
    """

    def __init__(self, adapter: Optional[BaseAdapter] = None) -> None:
        self._adapter = adapter or TOMLAdapter()

    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """Delegate to TOMLAdapter.load()."""
        return self._adapter.load(raw)
