"""
Concrete reader for JSON files.

Delegates parsing to ``JSONAdapter`` — contains no direct ``json`` usage.
"""

from typing import Any, Dict

from .base import BaseReader
from ..adapters.json_adapter import JSONAdapter


class JSONReader(BaseReader):
    """
    JSON reader — Template Method concrete participant.

    Implements ``_parse_content()`` by delegating to the JSONAdapter.
    All JSON-specific parsing logic lives in the adapter, not here.
    """

    def __init__(self) -> None:
        self._adapter = JSONAdapter()

    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """Delegate to JSONAdapter.load()."""
        return self._adapter.load(raw)
