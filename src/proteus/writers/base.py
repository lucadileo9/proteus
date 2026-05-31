"""
Template Method pattern — abstract base writer.

``write()`` is the template method that executes a fixed algorithm:
    1. _validate()    — check data type and output directory (common)
    2. _serialize()   — convert Dict IR → raw string        (VARIABLE — abstract)
    3. _write_file()  — write raw string to disk             (common)

Subclasses override only ``_serialize()``, delegating to their Adapter.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union


class BaseWriter(ABC):
    """
    Template Method — defines the fixed writing algorithm.

    The ``write()`` method runs three steps in a fixed sequence.
    Only step 2 (``_serialize``) is abstract; everything else is shared
    across all formats.

    Subclasses must:
        - Instantiate the matching Adapter in ``__init__``.
        - Implement ``_serialize()`` by calling ``self._adapter.dump(data)``.
    """

    # ------------------------------------------------------------------ #
    # Template Method (public — do NOT override)                          #
    # ------------------------------------------------------------------ #

    def write(self, data: Dict[str, Any], filepath: Union[str, Path]) -> None:
        """
        Template method — fixed writing algorithm.

        Args:
            data: Configuration data as Dict (IR).
            filepath: Destination file path.

        Raises:
            TypeError: If data is not a dict.
            FileNotFoundError: If the parent directory does not exist.
            ValueError: If the data cannot be serialized.
        """
        self._validate(data, filepath)
        content = self._serialize(data)
        self._write_file(content, filepath)

    # ------------------------------------------------------------------ #
    # Common steps (hooks — override only if truly needed)                #
    # ------------------------------------------------------------------ #

    def _validate(self, data: Dict[str, Any], filepath: Union[str, Path]) -> None:
        """Step 1 — verify data type and that the parent directory exists."""
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")
        parent = Path(filepath).parent
        if not parent.exists():
            raise FileNotFoundError(f"Directory not found: {parent}")

    # ------------------------------------------------------------------ #
    # Primitive operation (MUST be overridden by every subclass)          #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def _serialize(self, data: Dict[str, Any]) -> str:
        """
        Step 2 — convert the Dict IR into a format-specific string.

        Subclasses implement this by delegating to ``self._adapter.dump(data)``.

        Args:
            data: Configuration data as Dict[str, Any].

        Returns:
            Serialized string ready to be written to disk.
        """
        pass

    # ------------------------------------------------------------------ #
    # Hook (optional override)                                            #
    # ------------------------------------------------------------------ #

    def _write_file(self, content: str, filepath: Union[str, Path]) -> None:
        """Step 3 — write content to disk as UTF-8 text."""
        Path(filepath).write_text(content, encoding="utf-8")
