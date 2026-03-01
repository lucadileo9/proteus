"""
Adapter pattern (GoF) — Concrete adapter for .env files.

Adaptee: python-dotenv  (dotenv.dotenv_values)
Target:  BaseAdapter

.env format: flat KEY=value pairs, one entry per line.
Supports comments (#), single/double quotes, and the export prefix.

IR: Dict[str, str] — all values are strings (inherent to the format).
    Keys preserve the original casing from the file.
    Convention: keys are typically UPPER_CASE.
"""

import io
import shlex
from typing import Any, Dict

from dotenv import dotenv_values

from .base import BaseAdapter


class EnvAdapter(BaseAdapter):
    """
    Wraps python-dotenv (Adaptee) behind the BaseAdapter interface (Target).

    Note on the IR for .env files:
        The .env format is inherently flat: it does not support nesting.
        The resulting IR is therefore Dict[str, str] with all keys and
        values as plain strings.

        When dump() receives a nested dict (e.g. translated from JSON),
        nested keys are flattened using "__" as separator:
            {"database": {"host": "localhost"}} → DATABASE__HOST=localhost

    GoF roles:
        Target  → BaseAdapter
        Adapter → EnvAdapter             (this class)
        Adaptee → dotenv.dotenv_values    (python-dotenv)
    """

    def load(self, raw: str) -> Dict[str, Any]:
        """
        Delegate to dotenv_values(stream=...) and return the IR dict.

        Args:
            raw: Full text content of a .env file.

        Returns:
            Dict[str, str] with the KEY=value pairs from the file.
            Keys with no value (e.g. KEY=) are mapped to an empty string.

        Raises:
            ValueError: If raw cannot be parsed as a .env file.
        """
        try:
            parsed = dotenv_values(stream=io.StringIO(raw))
        except Exception as exc:
            raise ValueError(f"Invalid .env content: {exc}") from exc

        # dotenv_values may return None for keys with no assigned value
        return {k: (v if v is not None else "") for k, v in parsed.items()}

    def dump(self, data: Dict[str, Any]) -> str:
        """
        Serialize a Dict (IR) into .env KEY=value format.

        Nested dicts are flattened using "__" as separator:
            {'database': {'host': 'localhost'}} → DATABASE__HOST=localhost

        Non-string values are converted via str().
        Values containing spaces or special characters are automatically
        wrapped in double quotes.

        Args:
            data: Configuration dict (IR).

        Returns:
            String in .env format.
        """
        flat = self._flatten(data)
        lines = []
        for key, value in flat.items():
            str_value = str(value)
            # .env uses double quotes; quote manually instead of shlex.quote
            if self._needs_quoting(str_value):
                str_value = '"' + str_value.replace('"', '\\"') + '"'
            lines.append(f"{key}={str_value}")
        return "\n".join(lines) + ("\n" if lines else "")

    # ------------------------------------------------------------------ #
    # Private helpers                                                       #
    # ------------------------------------------------------------------ #

    def _flatten(
        self,
        data: Dict[str, Any],
        prefix: str = "",
    ) -> Dict[str, str]:
        """
        Recursively flatten a nested dict into a flat string dict.

        {'db': {'host': 'localhost', 'port': 5432}, 'debug': True}
        →  {'DB__HOST': 'localhost', 'DB__PORT': '5432', 'DEBUG': 'True'}
        """
        result: Dict[str, str] = {}
        for key, value in data.items():
            full_key = f"{prefix}__{key}".upper() if prefix else key.upper()
            if isinstance(value, dict):
                result.update(self._flatten(value, prefix=full_key))
            else:
                result[full_key] = str(value)
        return result

    @staticmethod
    def _needs_quoting(value: str) -> bool:
        """Return True if the value must be wrapped in double quotes."""
        # Quoting required for: empty string, spaces, =, #, $, newlines
        return (
            value == ""
            or any(c in value for c in (" ", "\t", "=", "#", "$", "\n", "'", '"'))
        )
