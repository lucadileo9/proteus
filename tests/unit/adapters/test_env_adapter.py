import pytest
from sample_data import SAMPLE_ENV, SAMPLE_FLAT

from proteus.adapters.env_adapter import EnvAdapter


class TestEnvAdapterLoad:
    """Tests for EnvAdapter.load()."""

    def setup_method(self):
        self.adapter = EnvAdapter()

    def test_load_valid(self):
        """load() parses valid .env content and returns the expected flat dict."""
        result = self.adapter.load(SAMPLE_ENV)
        assert result == SAMPLE_FLAT

    def test_load_returns_dict(self):
        """load() always returns a dict for valid .env content."""
        result = self.adapter.load("KEY=value\n")
        assert isinstance(result, dict)

    def test_load_values_are_strings(self):
        """All parsed values remain strings, even if they look numeric or boolean."""
        result = self.adapter.load("PORT=5432\nDEBUG=true\n")
        for v in result.values():
            assert isinstance(v, str)

    def test_load_ignores_comments(self):
        """load() skips lines starting with '#' as comments."""
        result = self.adapter.load("# comment\nKEY=value\n")
        assert result == {"KEY": "value"}
        assert not any(k.startswith("#") for k in result)

    def test_load_strips_quotes(self):
        """load() strips surrounding double quotes from values."""
        result = self.adapter.load('GREETING="hello world"\n')
        assert result["GREETING"] == "hello world"

    def test_load_empty_value(self):
        """load() handles KEY= with no value as an empty string."""
        result = self.adapter.load("EMPTY_KEY=\n")
        assert result["EMPTY_KEY"] == ""

    def test_load_empty_string(self):
        """load() returns an empty dict for an empty string."""
        assert self.adapter.load("") == {}

    def test_load_value_with_equals(self):
        """load() only splits on the first '=' so values may contain '='."""
        result = self.adapter.load("CONN=host=localhost;port=5432\n")
        assert result["CONN"] == "host=localhost;port=5432"


class TestEnvAdapterDump:
    """Tests for EnvAdapter.dump()."""

    def setup_method(self):
        self.adapter = EnvAdapter()

    def test_dump_flat(self):
        """dump() serializes flat data as KEY=value lines."""
        raw = self.adapter.dump(SAMPLE_FLAT)
        for key, value in SAMPLE_FLAT.items():
            assert f"{key.upper()}={value}" in raw

    def test_dump_nested_flattens(self):
        """dump() flattens nested dicts with '__' separator."""
        raw = self.adapter.dump({"db": {"host": "localhost"}})
        assert "DB__HOST=localhost" in raw

    def test_dump_deeply_nested(self):
        """dump() fully flattens deeply nested dicts."""
        raw = self.adapter.dump({"a": {"b": {"c": "deep"}}})
        assert "A__B__C=deep" in raw

    def test_dump_keys_uppercased(self):
        """dump() converts all keys to UPPER_CASE."""
        raw = self.adapter.dump({"myKey": "value"})
        assert "MYKEY=value" in raw

    def test_dump_quotes_spaces(self):
        """dump() wraps values containing spaces in double quotes."""
        raw = self.adapter.dump({"MSG": "hello world"})
        assert 'MSG="hello world"' in raw

    def test_dump_quotes_hash(self):
        """dump() wraps values containing '#' in double quotes."""
        raw = self.adapter.dump({"COLOR": "#ff0000"})
        assert 'COLOR="#ff0000"' in raw

    def test_dump_no_quotes_simple(self):
        """dump() does not quote simple values without special characters."""
        raw = self.adapter.dump({"KEY": "simple"})
        assert "KEY=simple" in raw
        assert '"simple"' not in raw

    def test_dump_boolean_to_string(self):
        """dump() converts boolean values to their string representation."""
        raw = self.adapter.dump({"DEBUG": True})
        assert "DEBUG=True" in raw

    def test_dump_numeric_to_string(self):
        """dump() converts numeric values to their string representation."""
        raw = self.adapter.dump({"PORT": 8080})
        assert "PORT=8080" in raw

    def test_dump_empty_dict(self):
        """dump() returns an empty string for an empty dict."""
        assert self.adapter.dump({}) == ""

    def test_dump_round_trip_flat(self):
        """Flat string data survives dump → load unchanged."""
        raw = self.adapter.dump(SAMPLE_FLAT)
        result = self.adapter.load(raw)
        assert result == SAMPLE_FLAT

    def test_dump_none_value_becomes_empty(self):
        """None values in the dict are converted to empty strings."""
        raw = self.adapter.dump({"KEY": None})
        assert "KEY=" in raw

    def test_load_non_string_raises_value_error(self):
        """load() raises ValueError if input is not a string."""
        with pytest.raises(ValueError, match="Invalid .env content"):
            self.adapter.load(123)  # type: ignore
