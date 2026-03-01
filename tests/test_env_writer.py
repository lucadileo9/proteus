"""
Tests for EnvWriter — Template Method concrete participant.

Covers:
    - Successful writing of flat data
    - Flattening of nested dicts with __ separator
    - Quoting of special values
    - Template Method validation steps
    - Round-trip consistency with EnvReader
"""

import pytest
from proteus.writers.env_writer import EnvWriter
from proteus.readers.env_reader import EnvReader
from sample_data import SAMPLE_FLAT, SAMPLE_NESTED


class TestEnvWriterWrite:
    """Test the Template Method write() flow for .env."""

    def setup_method(self):
        self.writer = EnvWriter()

    # ------------------------------------------------------------------ #
    # Happy path — flat data                                              #
    # ------------------------------------------------------------------ #

    def test_write_creates_file(self, tmp_path):
        """write() creates a file at the specified path."""
        path = str(tmp_path / ".env")
        self.writer.write(SAMPLE_FLAT, path)
        assert (tmp_path / ".env").exists()

    def test_write_flat_data(self, tmp_path):
        """write() writes flat KEY=value pairs correctly."""
        path = str(tmp_path / ".env")
        self.writer.write(SAMPLE_FLAT, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        for key, value in SAMPLE_FLAT.items():
            assert f"{key.upper()}={value}" in content

    def test_write_each_line_is_key_value(self, tmp_path):
        """Each non-empty line has the KEY=value format."""
        path = str(tmp_path / ".env")
        self.writer.write(SAMPLE_FLAT, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        for line in content.strip().splitlines():
            assert "=" in line

    # ------------------------------------------------------------------ #
    # Nested dict flattening                                              #
    # ------------------------------------------------------------------ #

    def test_write_nested_flattens_with_separator(self, tmp_path):
        """Nested dicts are flattened using __ separator."""
        path = str(tmp_path / ".env")
        data = {"database": {"host": "localhost", "port": 5432}}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "DATABASE__HOST=localhost" in content
        assert "DATABASE__PORT=5432" in content

    def test_write_nested_keys_uppercased(self, tmp_path):
        """Flattened keys are converted to UPPER_CASE."""
        path = str(tmp_path / ".env")
        data = {"app": {"debugMode": True}}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "APP__DEBUGMODE=True" in content

    def test_write_deeply_nested(self, tmp_path):
        """Deeply nested dicts are fully flattened."""
        path = str(tmp_path / ".env")
        data = {"a": {"b": {"c": "deep"}}}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "A__B__C=deep" in content

    # ------------------------------------------------------------------ #
    # Quoting                                                             #
    # ------------------------------------------------------------------ #

    def test_write_quotes_value_with_spaces(self, tmp_path):
        """Values with spaces are wrapped in double quotes."""
        path = str(tmp_path / ".env")
        data = {"GREETING": "hello world"}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert 'GREETING="hello world"' in content

    def test_write_quotes_value_with_hash(self, tmp_path):
        """Values with # are quoted to avoid being treated as comments."""
        path = str(tmp_path / ".env")
        data = {"COLOR": "#ff0000"}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert 'COLOR="#ff0000"' in content

    def test_write_simple_value_not_quoted(self, tmp_path):
        """Simple values without special chars are NOT quoted."""
        path = str(tmp_path / ".env")
        data = {"KEY": "simple"}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "KEY=simple" in content
        assert '"simple"' not in content

    # ------------------------------------------------------------------ #
    # Edge cases                                                          #
    # ------------------------------------------------------------------ #

    def test_write_empty_dict(self, tmp_path):
        """write() handles an empty dict."""
        path = str(tmp_path / ".env")
        self.writer.write({}, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert content == ""

    def test_write_boolean_values(self, tmp_path):
        """Boolean values are converted to strings."""
        path = str(tmp_path / ".env")
        data = {"DEBUG": True, "VERBOSE": False}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "DEBUG=True" in content
        assert "VERBOSE=False" in content

    def test_write_numeric_values(self, tmp_path):
        """Numeric values are converted to strings."""
        path = str(tmp_path / ".env")
        data = {"PORT": 8080, "RATE": 3.14}
        self.writer.write(data, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "PORT=8080" in content
        assert "RATE=3.14" in content

    def test_write_overwrites_existing(self, tmp_path):
        """write() overwrites an existing file."""
        path = str(tmp_path / ".env")
        self.writer.write({"OLD": "data"}, path)
        self.writer.write({"NEW": "data"}, path)
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "OLD" not in content
        assert "NEW=data" in content

    # ------------------------------------------------------------------ #
    # Round-trip with EnvReader (flat data)                               #
    # ------------------------------------------------------------------ #

    def test_round_trip_flat(self, tmp_path):
        """Flat data survives a write → read round-trip unchanged."""
        path = str(tmp_path / "roundtrip.env")
        self.writer.write(SAMPLE_FLAT, path)
        result = EnvReader().parse(path)
        assert result == SAMPLE_FLAT

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_write_non_dict_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is not a dict."""
        path = str(tmp_path / ".env")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write("not a dict", path)

    def test_write_list_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is a list."""
        path = str(tmp_path / ".env")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write([1, 2, 3], path)

    def test_write_none_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is None."""
        path = str(tmp_path / ".env")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write(None, path)

    def test_write_missing_directory(self, tmp_path):
        """write() raises FileNotFoundError if parent dir does not exist."""
        path = str(tmp_path / "nonexistent_dir" / ".env")
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            self.writer.write(SAMPLE_FLAT, path)


class TestEnvWriterStructure:
    """Verify structural properties of EnvWriter."""

    def test_has_adapter(self):
        """EnvWriter has a _adapter attribute."""
        writer = EnvWriter()
        assert hasattr(writer, "_adapter")

    def test_adapter_type(self):
        """The adapter is an EnvAdapter instance."""
        from proteus.adapters.env_adapter import EnvAdapter
        writer = EnvWriter()
        assert isinstance(writer._adapter, EnvAdapter)
