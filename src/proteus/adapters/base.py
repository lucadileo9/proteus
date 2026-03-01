from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAdapter(ABC):
    """
    Adapter pattern (GoF) — Target interface.

    Defines the uniform contract that all concrete adapters must fulfill.
    Readers and Writers depend exclusively on this abstraction, never on
    external libraries (Adaptees) directly. Swapping a library requires
    changes only inside the concrete adapter, nowhere else.

    GoF roles:
        Target  → BaseAdapter                  (this class)
        Adapter → JSONAdapter, YAMLAdapter, EnvAdapter, ...
        Adaptee → json, yaml, dotenv, ...      (external libraries)

    Internal representation (IR):
        Every load()  call returns Dict[str, Any].
        Every dump()  call accepts Dict[str, Any].
        Semantics depend on the format (e.g. .env is flat while
        JSON/YAML support nesting). Conversion logic lives in the
        concrete adapter, not in the Reader or Writer.
    """

    @abstractmethod
    def load(self, raw: str) -> Dict[str, Any]:
        """
        Parse a raw string in the format-specific encoding into the IR.

        Args:
            raw: Full text content of the configuration file.

        Returns:
            A Dict[str, Any] representing the parsed configuration.

        Raises:
            ValueError: If the raw content cannot be parsed.
        """
        pass

    @abstractmethod
    def dump(self, data: Dict[str, Any]) -> str:
        """
        Serialize the IR (a plain Python dict) into a format-specific string.

        Args:
            data: Configuration data as a plain Python dict.

        Returns:
            A string ready to be written to disk.

        Raises:
            ValueError: If the data cannot be serialized.
        """
        pass
