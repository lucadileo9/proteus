from typing import Any, Dict, cast

from .base import BaseWriter


class GenericWriter(BaseWriter):
    """
    Standard "bridge" writer that delegates all serialization to an injected adapter.

    Use this for formats that don't require specialized Template Method hooks.
    """

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Delegate serialization directly to the adapter."""
        return cast(str, self._adapter.dump(data))
