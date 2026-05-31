"""
Adapter pattern (GoF) — Concrete adapter for YAML.

Adaptee: yaml  (PyYAML)
Target:  BaseAdapter
"""

from typing import Any, Dict

import yaml

from .base import BaseAdapter


class YAMLAdapter(BaseAdapter):
    """
    Wraps PyYAML (Adaptee) behind the BaseAdapter interface (Target).

    Uses yaml.safe_load() instead of yaml.load() for security:
    it prevents arbitrary Python object deserialization.

    Shared by YAMLReader and YAMLWriter.

    GoF roles:
        Target  → BaseAdapter
        Adapter → YAMLAdapter        (this class)
        Adaptee → yaml (PyYAML)       yaml.safe_load / yaml.dump
    """

    def load(self, raw: str) -> Dict[str, Any]:
        """
        Delegate to yaml.safe_load() and return the IR dict.

        Args:
            raw: YAML-encoded string.

        Returns:
            Dict representing the parsed configuration.

        Raises:
            ValueError: If raw is not valid YAML or the root is not a mapping.
        """
        try:
            result = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML content: {exc}") from exc

        # Empty file or comments-only → safe_load returns None
        if result is None:
            return {}

        if not isinstance(result, dict):
            raise ValueError(
                f"YAML document root must be a mapping, got: {type(result).__name__}"
            )
        return result

    def dump(self, data: Dict[str, Any]) -> str:
        """
        Delegate to yaml.dump() and return the YAML string.

        Args:
            data: Configuration dict (IR).

        Returns:
            Human-readable YAML string (block style, unicode preserved).

        Raises:
            ValueError: If data cannot be serialized to YAML.
        """
        try:
            return yaml.dump(
                data,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
        except yaml.YAMLError as exc:
            raise ValueError(f"Cannot serialize to YAML: {exc}") from exc
