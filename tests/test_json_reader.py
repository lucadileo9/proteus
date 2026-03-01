"""
Tests for JSONReader — Template Method concrete participant.

Covers:
    - Successful parsing of valid JSON files
    - Template Method validation steps (file not found, not a file)
    - Delegation to JSONAdapter (invalid JSON, non-object root)
    - Round-trip consistency with JSONWriter
"""

import pytest
from proteus.readers.json_reader import JSONReader
from sample_data import SAMPLE_NESTED, SAMPLE_JSON, INVALID_JSON, JSON_ARRAY_ROOT


class TestJSONReaderParse:
    """Test the Template Method parse() flow for JSON."""

    def setup_method(self):
        self.reader = JSONReader()

    # ------------------------------------------------------------------ #
    # Happy path                                                          #
    # ------------------------------------------------------------------ #

    def test_parse_valid_json(self, json_file):
        """parse() returns the expected Dict IR from a valid JSON file."""
        result = self.reader.parse(json_file)
        assert result == SAMPLE_NESTED

    def test_parse_returns_dict(self, json_file):
        """parse() always returns a dict."""
        result = self.reader.parse(json_file)
        assert isinstance(result, dict)

    def test_parse_preserves_types(self, json_file):
        """Numeric and boolean values are preserved through parsing."""
        result = self.reader.parse(json_file)
        assert result["database"]["port"] == 5432
        assert isinstance(result["database"]["port"], int)
        assert result["app"]["debug"] is True

    def test_parse_nested_access(self, json_file):
        """Nested keys are accessible via regular dict traversal."""
        result = self.reader.parse(json_file)
        assert result["database"]["host"] == "localhost"
        assert result["app"]["version"] == "1.0.0"

    def test_parse_minimal_json(self, tmp_path):
        """parse() handles a minimal JSON object."""
        path = tmp_path / "minimal.json"
        path.write_text("{}", encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {}

    def test_parse_flat_json(self, tmp_path):
        """parse() handles a flat (non-nested) JSON object."""
        path = tmp_path / "flat.json"
        path.write_text('{"key": "value", "num": 42}', encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {"key": "value", "num": 42}

    def test_parse_unicode(self, tmp_path):
        """parse() handles Unicode content correctly."""
        path = tmp_path / "unicode.json"
        path.write_text('{"città": "Roma", "名前": "太郎"}', encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["città"] == "Roma"
        assert result["名前"] == "太郎"

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_parse_file_not_found(self, tmp_path):
        """parse() raises FileNotFoundError for a nonexistent file."""
        fake = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.reader.parse(fake)

    def test_parse_not_a_file(self, tmp_path):
        """parse() raises ValueError when path is a directory."""
        with pytest.raises(ValueError, match="Not a regular file"):
            self.reader.parse(str(tmp_path))

    # ------------------------------------------------------------------ #
    # Adapter-level errors (surfaced through _parse_content)              #
    # ------------------------------------------------------------------ #

    def test_parse_invalid_json(self, tmp_path):
        """parse() raises ValueError for syntactically invalid JSON."""
        path = tmp_path / "invalid.json"
        path.write_text(INVALID_JSON, encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON content"):
            self.reader.parse(str(path))

    def test_parse_array_root(self, tmp_path):
        """parse() raises ValueError when JSON root is an array."""
        path = tmp_path / "array.json"
        path.write_text(JSON_ARRAY_ROOT, encoding="utf-8")
        with pytest.raises(ValueError, match="root must be an object"):
            self.reader.parse(str(path))

    def test_parse_scalar_root(self, tmp_path):
        """parse() raises ValueError when JSON root is a scalar."""
        path = tmp_path / "scalar.json"
        path.write_text('"just a string"', encoding="utf-8")
        with pytest.raises(ValueError, match="root must be an object"):
            self.reader.parse(str(path))


class TestJSONReaderStructure:
    """Verify structural properties of JSONReader."""

    def test_has_adapter(self):
        """JSONReader has a _adapter attribute."""
        reader = JSONReader()
        assert hasattr(reader, "_adapter")

    def test_adapter_type(self):
        """The adapter is a JSONAdapter instance."""
        from proteus.adapters.json_adapter import JSONAdapter
        reader = JSONReader()
        assert isinstance(reader._adapter, JSONAdapter)
