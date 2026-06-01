import pytest
from sample_data import INVALID_TOML, SAMPLE_NESTED, SAMPLE_TOML, TOML_SCALAR_ROOT

from proteus.adapters.toml_adapter import TOMLAdapter


class TestTOMLAdapterLoad:
    """Tests for TOMLAdapter.load()."""

    def setup_method(self):
        self.adapter = TOMLAdapter()

    def test_load_valid(self):
        """load() parses valid TOML and returns the expected nested dict."""
        result = self.adapter.load(SAMPLE_TOML)
        assert result == SAMPLE_NESTED

    def test_load_returns_dict(self):
        """load() always returns a dict for a valid TOML document."""
        result = self.adapter.load('key = "value"\n')
        assert isinstance(result, dict)

    def test_load_preserves_types(self):
        """load() preserves int, float, and bool Python types."""
        result = self.adapter.load("n = 42\nf = 3.14\nb = true\n")
        assert result["n"] == 42
        assert isinstance(result["f"], float)
        assert result["b"] is True

    def test_load_unicode(self):
        """load() handles Unicode keys and values correctly."""
        result = self.adapter.load('"città" = "Roma"\n')
        assert result["città"] == "Roma"

    def test_load_invalid_toml(self):
        """load() raises ValueError for syntactically invalid TOML."""
        with pytest.raises(ValueError, match="Invalid TOML content"):
            self.adapter.load(INVALID_TOML)

    def test_load_scalar_root(self):
        """load() raises ValueError when TOML root is a scalar."""
        with pytest.raises(ValueError, match="Invalid TOML content"):
            self.adapter.load(TOML_SCALAR_ROOT)


class TestTOMLAdapterDump:
    """Tests for TOMLAdapter.dump()."""

    def setup_method(self):
        self.adapter = TOMLAdapter()

    def test_dump_valid(self):
        """dump() produces valid TOML that parses back to the original dict."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        # Use adapter's own load to verify
        assert self.adapter.load(raw) == SAMPLE_NESTED

    def test_dump_unicode_preserved(self):
        """dump() preserves Unicode characters in keys and values."""
        raw = self.adapter.dump({"città": "Roma"})
        assert "Roma" in raw
        assert "città" in raw

    def test_dump_empty_dict(self):
        """dump() serializes an empty dict to valid empty TOML."""
        raw = self.adapter.dump({})
        assert self.adapter.load(raw) == {}

    def test_dump_round_trip(self):
        """Data survives a dump() → load() round-trip unchanged."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        assert self.adapter.load(raw) == SAMPLE_NESTED
