"""
ConfigurationManager — Facade with optional Singleton support.

This is the central entry point of the Proteus library.

Optional Singleton pattern:
    ``instance()`` returns a shared, thread-safe singleton when a
    global manager is desired. Direct construction via ``ConfigurationManager()``
    returns a regular independent instance.

Facade pattern:
    ``load()``, ``get()``, ``merge()``, ``translate()`` hide the full
    complexity of Factory Method, Template Method, and Adapter from
    the client code.

Typical usage::

    from proteus import ConfigurationManager

    config = ConfigurationManager()
    config.load("base.yaml")
    config.merge("production.yaml")       # deep-merge on top
    print(config.get("database.host"))    # dot-notation access
    config.translate("base.yaml", "base.json")   # format conversion
"""

import copy
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .exceptions import (
    ConfigurationNotLoadedError,
    UnsupportedFormatError,
)
from .formats.base_format import FormatCreator
from .formats.env_format import EnvFormatCreator
from .formats.json_format import JSONFormatCreator
from .formats.yaml_format import YAMLFormatCreator


class ConfigurationManager:
    """
    Facade for unified configuration management with optional Singleton access.

    Responsibilities:
        - Maintain a single global configuration state (IR: ``Dict``)
        - Select the correct ``FormatCreator`` based on file extension
        - Coordinate reading via Reader (through Factory Method)
        - Deep-merge multiple configuration sources
        - Provide unified dot-notation access
        - Translate between formats

    Design-pattern roles:
        **Singleton** – ``instance()`` with ``threading.Lock``
        **Facade**    – public methods encapsulate the entire pattern stack
    """

    # These are class-level attributes for the optional singleton access.
    _instance: Optional["ConfigurationManager"] = None # this represents the single instance of the class, initially None
    _lock: threading.Lock = threading.Lock() # lock to ensure thread-safe singleton creation

    # ------------------------------------------------------------------ #
    # Singleton                                                           #
    # ------------------------------------------------------------------ #

    @classmethod
    def instance(cls) -> "ConfigurationManager":
        """
        Return a shared singleton instance with double-check locking.

        First check is lock-free (fast path for the common case).
        Second check (inside the lock) prevents race conditions.

        Direct construction via ``ConfigurationManager()`` remains available
        for callers that want isolated instances.
        """
        if cls._instance is None: # check if instance already exists (fast path)
            with cls._lock: # if it doesn't exist, acquire lock to create it
                if cls._instance is None: # double-check if instance was created while waiting for lock
                    cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        # Dictionary to hold the configuration data (IR)
        self._config: Dict[str, Any] = {}
        # List to track loaded files (for debugging/auditing)
        self._loaded_files: List[str] = []
        # Registry mapping file extensions to FormatCreators
        self._creators: Dict[str, FormatCreator] = {}
        self._register_default_creators() # Register built-in creators for JSON, YAML, and ENV

    def __enter__(self) -> "ConfigurationManager":
        """Enter a context manager scope and return this manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Reset transient state when leaving a context manager scope."""
        self.reset()
        return False

    @classmethod
    def temporary(cls) -> "ConfigurationManager":
        """Create a fresh manager intended for use inside a `with` block."""
        return cls()

    # ------------------------------------------------------------------ #
    # Creator registry                                                    #
    # ------------------------------------------------------------------ #

    def _register_default_creators(self) -> None:
        """Register built-in FormatCreators for JSON, YAML, and ENV."""
        for creator in (
            JSONFormatCreator(),
            YAMLFormatCreator(),
            EnvFormatCreator(),
        ):
            for ext in creator.get_extensions():
                self._creators[ext] = creator

    def register_creator(self, creator: FormatCreator) -> None:
        """
        Register a custom FormatCreator.

        This allows third-party formats (TOML, INI, …) to be plugged in
        without modifying any existing code (Open/Closed Principle).

        Args:
            creator: A ``FormatCreator`` subclass instance.
        """
        for ext in creator.get_extensions():
            self._creators[ext] = creator

    def _get_creator(self, filepath: Union[str, Path]) -> FormatCreator:
        """
        Select the FormatCreator whose extensions match *filepath*.

        Args:
            filepath: Path to a configuration file.

        Returns:
            The matching ``FormatCreator``.

        Raises:
            UnsupportedFormatError: If no creator is registered for the extension.
        """
        ext = Path(filepath).suffix.lower()
        creator = self._creators.get(ext)
        if creator is None:
            supported = ", ".join(sorted(self._creators.keys()))
            raise UnsupportedFormatError(
                f"Format '{ext}' is not supported. "
                f"Available: {supported}"
            )
        return creator

    # ------------------------------------------------------------------ #
    # Facade — public API                                                 #
    # ------------------------------------------------------------------ #

    def load(self, filepath: Union[str, Path]) -> None:
        """
        Load a configuration file and deep-merge it into the IR.

        Args:
            filepath: Path to the configuration file.

        Raises:
            UnsupportedFormatError: Unknown extension.
            FileNotFoundError: File does not exist.
            ValueError: Content cannot be parsed.
        """
        creator = self._get_creator(filepath) # select the appropriate FormatCreator based on the file extension
        reader = creator.create_reader() # use the creator to create a Reader instance
        new_config = reader.parse(filepath) # parse the file to get a new configuration dictionary
        self._config = self._deep_merge(self._config, new_config) # deep-merge the new configuration into the existing one
        self._loaded_files.append(str(Path(filepath).resolve())) # track the loaded file (store absolute path for clarity)

    def merge(self, filepath: Union[str, Path]) -> None:
        """
        Alias for ``load()`` — semantically clearer for explicit merges.

        Merges the contents of *filepath* on top of the current IR
        (values in the new file win on conflict).
        """
        self.load(filepath)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Access a configuration value via dot-notation.

        Args:
            key: Dot-separated key path (e.g. ``"database.host"``).
            default: Value to return if the key is not found.

        Returns:
            The configuration value, or *default*.

        Raises:
            ConfigurationNotLoadedError: If no file has been loaded yet.
        """
        if not self._config:
            raise ConfigurationNotLoadedError(
                "No configuration loaded. Call load() first."
            )

        parts = key.split(".")
        value: Any = self._config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value

    def get_all(self) -> Dict[str, Any]:
        """Return a shallow copy of the entire IR."""
        return self._config.copy()

    def translate(self, input_path: str, output_path: str) -> None:
        """
        Convert a configuration file from one format to another.

        This is where **all five patterns collaborate**:

        1. **Facade** — ``translate()`` hides the orchestration.
        2. **Factory Method** — ``_get_creator()`` selects creators.
        3. **Template Method** — ``reader.parse()`` / ``writer.write()``.
        4. **Adapter** — ``load()`` / ``dump()`` inside readers/writers.
        5. **Singleton** — the client calls this on a unique instance.

        Args:
            input_path:  Path to the source file.
            output_path: Path to the destination file.

        Raises:
            UnsupportedFormatError: Unknown extension for either path.
            FileNotFoundError: Source file does not exist or dest dir missing.
            ValueError: Content cannot be parsed or serialized.
        """
        in_creator = self._get_creator(input_path) # select the appropriate FormatCreator for the input file
        out_creator = self._get_creator(output_path) # select the appropriate FormatCreator for the output file

        reader = in_creator.create_reader() # create a Reader instance for the input format
        writer = out_creator.create_writer() # create a Writer instance for the output format

        data = reader.parse(input_path) # parse the input file to get the configuration data as a dictionary
        writer.write(data, output_path) # write the configuration data to the output file in the new format

    def translate_and_load(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> None:
        """
        Translate a configuration file and then load the translated output.

        This is useful when you want the conversion result to become part of
        the manager state immediately after the file is written.
        """
        self.translate(input_path, output_path)
        self.load(output_path)

    # ------------------------------------------------------------------ #
    # Housekeeping                                                        #
    # ------------------------------------------------------------------ #

    def loaded_files(self) -> List[str]:
        """Return a COPY of the loaded-file list."""
        return self._loaded_files.copy() # Use copy to prevent external mutation

    def reset(self) -> None:
        """
        Clear the internal state (config + loaded-files).

        Useful for testing.  Does **not** destroy the singleton itself.
        """
        self._config = {}
        self._loaded_files = []

    @classmethod
    def _destroy(cls) -> None:
        """
        Destroy the singleton instance entirely.

        **For testing only** — allows fresh construction in each test.
        """
        with cls._lock:
            cls._instance = None

    # ------------------------------------------------------------------ #
    # Deep-merge helper                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _deep_merge(
        base: Dict[str, Any],
        override: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Recursively merge *override* into *base*.

        Scalar values in *override* win.  Nested dicts are merged
        recursively — neither side is mutated.
        """
        result = base.copy() # start with a shallow copy of the base
        for key, value in override.items(): # iterate over the new dictionary
            if (
                key in result # if the key exists in the base
                and isinstance(result[key], dict) # and the corresponding value in the base is a dict
                and isinstance(value, dict) # and the value in the override is also a dict
            ):
                # recursively merge the nested dictionaries
                result[key] = ConfigurationManager._deep_merge(
                    result[key], value
                )
            else:
                # instead if the key doesn't exist in the base, or either value is not a dict, override it directly
                result[key] = value
        return result
