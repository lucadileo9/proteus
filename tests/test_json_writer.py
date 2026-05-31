"""
Tests for JSONWriter — Template Method concrete participant.

Covers:
    - Successful writing of valid data
    - Output format correctness (valid JSON, indentation, unicode)
    - Template Method validation steps (non-dict data, missing directory)
    - Round-trip consistency with JSONReader
"""

import json

import pytest
from sample_data import SAMPLE_NESTED

from proteus.readers.json_reader import JSONReader
from proteus.writers.json_writer import JSONWriter


class TestJSONWriterWrite:
    """Test the Template Method write() flow for JSON."""

    def setup_method(self):
        self.writer = JSONWriter()

    # ------------------------------------------------------------------ #
    # Happy path                                                          #
    # ------------------------------------------------------------------ #

    def test_write_creates_file(self, tmp_path):
        """write() creates a file at the specified path."""
        path = str(tmp_path / "output.json")
        self.writer.write(SAMPLE_NESTED, path)
        assert (tmp_path / "output.json").exists()

    def test_write_valid_json_output(self, tmp_path):
        """The written file contains valid JSON."""
        path = str(tmp_path / "output.json")
        self.writer.write(SAMPLE_NESTED, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert parsed == SAMPLE_NESTED

    def test_write_preserves_types(self, tmp_path):
        """Numeric and boolean values are preserved in the output."""
        path = str(tmp_path / "output.json")
        self.writer.write(SAMPLE_NESTED, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert parsed["database"]["port"] == 5432
        assert parsed["app"]["debug"] is True

    def test_write_indented(self, tmp_path):
        """Output is pretty-printed with indentation."""
        path = str(tmp_path / "output.json")
        self.writer.write({"key": "value"}, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        # Should contain newlines (not single-line)
        assert "\n" in content

    def test_write_unicode(self, tmp_path):
        """Unicode characters are preserved (not escaped)."""
        path = str(tmp_path / "output.json")
        data = {"città": "Roma", "名前": "太郎"}
        self.writer.write(data, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        assert "Roma" in content
        assert "太郎" in content

    def test_write_empty_dict(self, tmp_path):
        """write() handles an empty dict."""
        path = str(tmp_path / "output.json")
        self.writer.write({}, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        assert json.loads(content) == {}

    def test_write_overwrites_existing(self, tmp_path):
        """write() overwrites an existing file."""
        path = str(tmp_path / "output.json")
        self.writer.write({"old": "data"}, path)
        self.writer.write({"new": "data"}, path)
        content = (tmp_path / "output.json").read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert parsed == {"new": "data"}

    def test_write_path_object(self, tmp_path):
        """write() accepts pathlib.Path objects."""
        path = tmp_path / "output.json"
        self.writer.write(SAMPLE_NESTED, path)
        assert path.exists()

    # ------------------------------------------------------------------ #
    # Round-trip with JSONReader                                          #
    # ------------------------------------------------------------------ #

    def test_round_trip(self, tmp_path):
        """Data survives a write → read round-trip unchanged."""
        path = str(tmp_path / "roundtrip.json")
        self.writer.write(SAMPLE_NESTED, path)
        result = JSONReader().parse(path)
        assert result == SAMPLE_NESTED

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_write_non_dict_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is not a dict."""
        path = str(tmp_path / "output.json")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write("not a dict", path)

    def test_write_list_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is a list."""
        path = str(tmp_path / "output.json")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write([1, 2, 3], path)

    def test_write_none_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is None."""
        path = str(tmp_path / "output.json")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write(None, path)

    def test_write_missing_directory(self, tmp_path):
        """write() raises FileNotFoundError if parent dir does not exist."""
        path = str(tmp_path / "nonexistent_dir" / "output.json")
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            self.writer.write(SAMPLE_NESTED, path)


class TestJSONWriterStructure:
    """Verify structural properties of JSONWriter."""

    def test_has_adapter(self):
        """JSONWriter has a _adapter attribute."""
        writer = JSONWriter()
        assert hasattr(writer, "_adapter")

    def test_adapter_type(self):
        """The adapter is a JSONAdapter instance."""
        from proteus.adapters.json_adapter import JSONAdapter

        writer = JSONWriter()
        assert isinstance(writer._adapter, JSONAdapter)
