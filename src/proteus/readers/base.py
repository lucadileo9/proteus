"""
Template Method pattern — abstract base reader.

``parse()`` is the template method that executes a fixed algorithm:
    1. _validate()       — check that the file exists (common)
    2. _read_file()      — read raw text from disk    (common)
    3. _parse_content()  — convert raw text → Dict IR (VARIABLE — abstract)
    4. _normalize_data() — optional post-processing   (common hook)

Subclasses override only ``_parse_content()``, delegating to their Adapter.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union


class BaseReader(ABC):
    """
    Template Method — defines the fixed reading algorithm.

    The ``parse()`` method runs four steps in a fixed sequence.
    Only step 3 (``_parse_content``) is abstract; everything else
    is shared across all formats and should rarely need overriding.

    Subclasses must:
        - Instantiate the matching Adapter in ``__init__``.
        - Implement ``_parse_content()`` by calling ``self._adapter.load(raw)``.
    """

    # ------------------------------------------------------------------ #
    # Template Method (public — do NOT override)                          #
    # ------------------------------------------------------------------ #

    def parse(self, filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Template method — fixed parsing algorithm.

        Args:
            filepath: Path to the configuration file.

        Returns:
            Parsed configuration as a Dict (IR).

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file path is not a regular file or
                the content cannot be parsed.
        """
        self._validate(filepath)
        raw = self._read_file(filepath)
        data = self._parse_content(raw)
        return self._normalize_data(data)

    # ------------------------------------------------------------------ #
    # Common steps (hooks — override only if truly needed)                #
    # ------------------------------------------------------------------ #

    def _validate(self, filepath: Union[str, Path]) -> None:
        """Step 1 — verify that the file exists and is a regular file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if not path.is_file():
            raise ValueError(f"Not a regular file: {filepath}")

    def _read_file(self, filepath: Union[str, Path]) -> str:
        """Step 2 — read the full file content as UTF-8 text."""
        return Path(filepath).read_text(encoding="utf-8")

    # ------------------------------------------------------------------ #
    # Primitive operation (MUST be overridden by every subclass)          #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def _parse_content(self, raw: str) -> Dict[str, Any]:
        """
        Step 3 — convert raw text into the Dict IR.

        Subclasses implement this by delegating to ``self._adapter.load(raw)``.

        Args:
            raw: Full text content of the file.

        Returns:
            Parsed configuration as Dict[str, Any].
        """
        pass

    # ------------------------------------------------------------------ #
    # Hook (optional override)                                            #
    # ------------------------------------------------------------------ #

    def _normalize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4 — optional post-processing.

        Default implementation returns data unchanged.
        Override if a format needs extra normalization after parsing.
        """
        return data
