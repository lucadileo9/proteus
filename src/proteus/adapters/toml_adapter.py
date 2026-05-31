import sys
from typing import Any, Dict, cast

from .base import BaseAdapter

# Handle TOML parsing based on Python version
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


class TOMLAdapter(BaseAdapter):
    """
    Adapter for TOML configuration format.

    Uses the standard library ``tomllib`` (Python 3.11+) or the ``tomli``
    backport for parsing, and ``tomli-w`` for serialization.
    """

    def load(self, raw: str) -> Dict[str, Any]:
        """
        Parse a TOML string into a dictionary.

        Args:
            raw: TOML formatted string.

        Returns:
            A dictionary representation of the TOML data.

        Raises:
            ValueError: If the TOML is invalid.
        """
        try:
            data = tomllib.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("TOML root must be a dictionary")
            return cast(Dict[str, Any], data)
        except Exception as e:
            raise ValueError(f"Invalid TOML content: {e}") from e

    def dump(self, data: Dict[str, Any]) -> str:
        """
        Serialize a dictionary into a TOML string.

        Args:
            data: Dictionary to serialize.

        Returns:
            A TOML formatted string.

        Raises:
            TypeError: If data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("TOML serialization requires a dictionary at the root")
        return cast(str, tomli_w.dumps(data))
