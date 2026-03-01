"""
Tests for EnvReader — Template Method concrete participant.

Covers:
    - Successful parsing of valid .env files
    - Edge cases (comments, empty values, quoted values, empty file)
    - Template Method validation steps
    - Delegation to EnvAdapter
"""

import pytest
from proteus.readers.env_reader import EnvReader
from sample_data import (
    SAMPLE_FLAT,
    SAMPLE_ENV,
    ENV_WITH_QUOTES,
    ENV_WITH_COMMENTS,
    ENV_EMPTY_VALUE,
    ENV_EMPTY,
)


class TestEnvReaderParse:
    """Test the Template Method parse() flow for .env."""

    def setup_method(self):
        self.reader = EnvReader()

    # ------------------------------------------------------------------ #
    # Happy path                                                          #
    # ------------------------------------------------------------------ #

    def test_parse_valid_env(self, env_file):
        """parse() returns the expected Dict IR from a valid .env file."""
        result = self.reader.parse(env_file)
        assert result == SAMPLE_FLAT

    def test_parse_returns_dict(self, env_file):
        """parse() always returns a dict."""
        result = self.reader.parse(env_file)
        assert isinstance(result, dict)

    def test_parse_values_are_strings(self, env_file):
        """All values in .env IR are strings."""
        result = self.reader.parse(env_file)
        for value in result.values():
            assert isinstance(value, str)

    def test_parse_preserves_key_case(self, env_file):
        """Keys preserve their original casing from the file."""
        result = self.reader.parse(env_file)
        assert "DB_HOST" in result
        assert "APP_NAME" in result

    # ------------------------------------------------------------------ #
    # Edge cases                                                          #
    # ------------------------------------------------------------------ #

    def test_parse_with_comments(self, tmp_path):
        """parse() ignores comment lines (starting with #)."""
        path = tmp_path / ".env"
        path.write_text(ENV_WITH_COMMENTS, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {"DB_HOST": "localhost", "APP_NAME": "Proteus"}
        # Comments must not appear as keys
        assert not any(k.startswith("#") for k in result)

    def test_parse_with_quotes(self, tmp_path):
        """parse() strips surrounding quotes from values."""
        path = tmp_path / ".env"
        path.write_text(ENV_WITH_QUOTES, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["GREETING"] == "hello world"
        assert result["PATH_VAR"] == "/usr/local/bin"

    def test_parse_empty_value(self, tmp_path):
        """parse() handles KEY= with no value (empty string)."""
        path = tmp_path / ".env"
        path.write_text(ENV_EMPTY_VALUE, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["EMPTY_KEY"] == ""

    def test_parse_empty_file(self, tmp_path):
        """parse() returns empty dict for an empty .env file."""
        path = tmp_path / ".env"
        path.write_text(ENV_EMPTY, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {}

    def test_parse_single_entry(self, tmp_path):
        """parse() handles a single KEY=value line."""
        path = tmp_path / ".env"
        path.write_text("ONLY_KEY=only_value\n", encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {"ONLY_KEY": "only_value"}

    def test_parse_value_with_equals(self, tmp_path):
        """parse() handles values containing '=' characters."""
        path = tmp_path / ".env"
        path.write_text("CONN=host=localhost;port=5432\n", encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["CONN"] == "host=localhost;port=5432"

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_parse_file_not_found(self, tmp_path):
        """parse() raises FileNotFoundError for a nonexistent file."""
        fake = str(tmp_path / "nonexistent.env")
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.reader.parse(fake)

    def test_parse_not_a_file(self, tmp_path):
        """parse() raises ValueError when path is a directory."""
        with pytest.raises(ValueError, match="Not a regular file"):
            self.reader.parse(str(tmp_path))


class TestEnvReaderStructure:
    """Verify structural properties of EnvReader."""

    def test_has_adapter(self):
        """EnvReader has a _adapter attribute."""
        reader = EnvReader()
        assert hasattr(reader, "_adapter")

    def test_adapter_type(self):
        """The adapter is an EnvAdapter instance."""
        from proteus.adapters.env_adapter import EnvAdapter
        reader = EnvReader()
        assert isinstance(reader._adapter, EnvAdapter)
