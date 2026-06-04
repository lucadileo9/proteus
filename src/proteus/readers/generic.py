from typing import Any, Dict, cast

from .base import BaseReader


class GenericReader(BaseReader):
    """
    Standard "bridge" reader that delegates all parsing to an injected adapter.

    Use this for formats that don't require specialized Template Method hooks.
    """

    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """Delegate parsing directly to the adapter."""
        return cast(Dict[str, Any], self._adapter.load(raw))
