import json

import pytest
from sample_data import INVALID_JSON, JSON_ARRAY_ROOT, SAMPLE_JSON, SAMPLE_NESTED

from proteus.adapters.json_adapter import JSONAdapter


class TestJSONAdapterLoad:
    """Tests for JSONAdapter.load()."""

    def setup_method(self):
        self.adapter = JSONAdapter()

    def test_load_valid(self):
        """load() parses valid JSON and returns the expected nested dict."""
        result = self.adapter.load(SAMPLE_JSON)
        assert result == SAMPLE_NESTED

    def test_load_returns_dict(self):
        """load() always returns a dict for a valid JSON object."""
        result = self.adapter.load('{"key": "value"}')
        assert isinstance(result, dict)

    def test_load_preserves_types(self):
        """load() preserves int, float, bool, and null Python types."""
        result = self.adapter.load('{"n": 42, "f": 3.14, "b": true, "x": null}')
        assert result["n"] == 42
        assert isinstance(result["f"], float)
        assert result["b"] is True
        assert result["x"] is None

    def test_load_unicode(self):
        """load() handles Unicode keys and values correctly."""
        result = self.adapter.load('{"città": "Roma"}')
        assert result["città"] == "Roma"

    def test_load_empty_object(self):
        """load() returns an empty dict for an empty JSON object."""
        assert self.adapter.load("{}") == {}

    def test_load_invalid_json(self):
        """load() raises ValueError for syntactically invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON content"):
            self.adapter.load(INVALID_JSON)

    def test_load_array_root(self):
        """load() raises ValueError when JSON root is an array."""
        with pytest.raises(ValueError, match="root must be an object"):
            self.adapter.load(JSON_ARRAY_ROOT)

    def test_load_scalar_root(self):
        """load() raises ValueError when JSON root is a string scalar."""
        with pytest.raises(ValueError, match="root must be an object"):
            self.adapter.load('"just a string"')

    def test_load_number_root(self):
        """load() raises ValueError when JSON root is a number."""
        with pytest.raises(ValueError, match="root must be an object"):
            self.adapter.load("42")


class TestJSONAdapterDump:
    """Tests for JSONAdapter.dump()."""

    def setup_method(self):
        self.adapter = JSONAdapter()

    def test_dump_valid(self):
        """dump() produces valid JSON that parses back to the original dict."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        parsed = json.loads(raw)
        assert parsed == SAMPLE_NESTED

    def test_dump_pretty_printed(self):
        """dump() output is pretty-printed with newlines."""
        raw = self.adapter.dump({"key": "value"})
        assert "\n" in raw  # not single-line

    def test_dump_unicode_preserved(self):
        """dump() preserves Unicode characters without ASCII-escaping."""
        raw = self.adapter.dump({"città": "Roma"})
        assert "Roma" in raw
        assert "città" in raw
        assert "\\u" not in raw  # must NOT be ascii-escaped

    def test_dump_empty_dict(self):
        """dump() serializes an empty dict to a valid empty JSON object."""
        raw = self.adapter.dump({})
        assert json.loads(raw) == {}

    def test_dump_round_trip(self):
        """Data survives a dump() → load() round-trip unchanged."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        assert self.adapter.load(raw) == SAMPLE_NESTED

    def test_dump_unserializable_raises_value_error(self):
        """dump() raises ValueError for non-serializable objects (like set)."""
        data = {"key": {1, 2, 3}}  # sets are not JSON serializable
        with pytest.raises(ValueError, match="Cannot serialize to JSON"):
            self.adapter.dump(data)
