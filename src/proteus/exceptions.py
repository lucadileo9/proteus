"""
Custom exceptions for Proteus configuration library.

This module defines the exception hierarchy used throughout Proteus
for handling configuration-related errors.

Exception Hierarchy:
    ConfigurationError (base)
    ├── UnsupportedFormatError
    ├── InvalidKeyError
    └── ConfigurationNotLoadedError
"""


class ConfigurationError(Exception):
    """
    Base exception for all Proteus configuration errors.

    All custom exceptions in Proteus inherit from this base class,
    allowing users to catch all library-specific errors with a single
    except clause if desired.

    Example:
        try:
            config.load('settings.json')
        except ConfigurationError as e:
            print(f"Configuration error: {e}")
    """

    pass


class UnsupportedFormatError(ConfigurationError):
    """
    Raised when attempting to load a file with unsupported format.

    This exception is raised by ConfigParserFactory when no parser
    is registered for the given file extension.

    Example:
        >>> config.load('settings.xml')  # If XML parser not registered
        UnsupportedFormatError: Format '.xml' is not supported

    Attributes:
        extension: The unsupported file extension
        message: Error message
    """

    pass


class InvalidKeyError(ConfigurationError):
    """
    Raised when attempting to access an invalid configuration key.

    This exception may be raised when a configuration key doesn't
    conform to expected format or contains invalid characters.

    Example:
        >>> config.get('invalid..key')  # Double dots invalid
        InvalidKeyError: Key 'invalid..key' is not valid

    Attributes:
        key: The invalid key that was attempted
        message: Error message
    """

    pass


class ConfigurationNotLoadedError(ConfigurationError):
    """
    Raised when attempting to access configuration before loading any files.

    This exception is raised by ConfigurationManager.get() when called
    before any configuration has been loaded via load().

    Example:
        >>> config = ConfigurationManager()
        >>> config.get('database.host')  # No config loaded yet
        ConfigurationNotLoadedError: No configuration loaded yet

    Note:
        Always call load() or load_multiple() before attempting to
        retrieve configuration values.
    """

    pass


class ConfigurationTypeError(ConfigurationError):
    """
    Raised when a configuration value fails to cast to the specified type.

    This exception is raised by ConfigurationManager.get(key, cast=...)
    when the cast function raises a ValueError or TypeError.

    Example:
        >>> config.get('port', cast=int)  # where port is "abc"
        ConfigurationTypeError: Cannot cast value 'abc' for key 'port' to expected type.
    """

    pass
