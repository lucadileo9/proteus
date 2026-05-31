"""
Adapter pattern (GoF) — Concrete adapter for JSON.

Adaptee: json  (Python standard library)
Target:  BaseAdapter
"""

import json
from typing import Any, Dict

from .base import BaseAdapter


class JSONAdapter(BaseAdapter):
    """
    Wraps the json stdlib module (Adaptee) behind the BaseAdapter interface (Target).

    Shared by JSONReader and JSONWriter: replacing the underlying library
    (e.g. switching to orjson) requires changes only here.

    GoF roles:
        Target  → BaseAdapter
        Adapter → JSONAdapter        (this class)
        Adaptee → json (stdlib)       json.loads / json.dumps
    """

    def load(self, raw: str) -> Dict[str, Any]:
        """
        Delegate to json.loads() and return the IR dict.

        Args:
            raw: JSON-encoded string.

        Returns:
            Dict representing the parsed configuration.

        Raises:
            ValueError: If raw is not valid JSON or the root is not an object.
        """
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON content: {exc}") from exc

        if not isinstance(result, dict):
            raise ValueError(
                f"JSON document root must be an object, got: {type(result).__name__}"
            )
        return result

    def dump(self, data: Dict[str, Any]) -> str:
        """
        Delegate to json.dumps() and return the JSON string.

        Args:
            data: Configuration dict (IR).

        Returns:
            Pretty-printed JSON string (2-space indent, unicode preserved).

        Raises:
            ValueError: If data cannot be serialized to JSON.
        """
        try:
            return json.dumps(data, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Cannot serialize to JSON: {exc}") from exc
