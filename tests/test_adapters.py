"""
Tests for the Adapter Layer — Adapter pattern (GoF canonical).

Covers every concrete adapter (JSONAdapter, YAMLAdapter, EnvAdapter):
    - load() happy-path and error cases
    - dump() happy-path and edge cases
    - Round-trip load(dump(data)) == data
    - BaseAdapter cannot be instantiated directly
"""

import json

import pytest
import yaml
from sample_data import (
    INVALID_JSON,
    INVALID_YAML,
    JSON_ARRAY_ROOT,
    SAMPLE_ENV,
    SAMPLE_FLAT,
    SAMPLE_JSON,
    SAMPLE_NESTED,
    SAMPLE_YAML,
    YAML_EMPTY,
    YAML_ONLY_COMMENTS,
    YAML_SCALAR_ROOT,
)

from proteus.adapters.base import BaseAdapter
from proteus.adapters.env_adapter import EnvAdapter
from proteus.adapters.json_adapter import JSONAdapter
from proteus.adapters.toml_adapter import TOMLAdapter
from proteus.adapters.yaml_adapter import YAMLAdapter

# ================================================================== #
# BaseAdapter — abstract target                                       #
# ================================================================== #


class TestBaseAdapterAbstract:
    """Verify that BaseAdapter cannot be instantiated directly."""

    def test_cannot_instantiate(self):
        """Instantiating BaseAdapter directly raises TypeError."""
        with pytest.raises(TypeError):
            BaseAdapter()

    def test_abstract_methods(self):
        """BaseAdapter declares load() and dump() as abstract methods."""
        abstracts = BaseAdapter.__abstractmethods__
        assert "load" in abstracts
        assert "dump" in abstracts

    def test_subclass_missing_method(self):
        """A subclass that only implements load() is still abstract."""

        class Incomplete(BaseAdapter):
            def load(self, raw):
                return {}

        with pytest.raises(TypeError):
            Incomplete()


# ================================================================== #
# JSONAdapter                                                         #
# ================================================================== #


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


# ================================================================== #
# YAMLAdapter                                                         #
# ================================================================== #


class TestYAMLAdapterLoad:
    """Tests for YAMLAdapter.load()."""

    def setup_method(self):
        self.adapter = YAMLAdapter()

    def test_load_valid(self):
        """load() parses valid YAML and returns the expected nested dict."""
        result = self.adapter.load(SAMPLE_YAML)
        assert result == SAMPLE_NESTED

    def test_load_returns_dict(self):
        """load() always returns a dict for a valid YAML mapping."""
        result = self.adapter.load("key: value\n")
        assert isinstance(result, dict)

    def test_load_preserves_types(self):
        """load() preserves int, float, and bool Python types."""
        result = self.adapter.load("n: 42\nf: 3.14\nb: true\n")
        assert result["n"] == 42
        assert isinstance(result["f"], float)
        assert result["b"] is True

    def test_load_unicode(self):
        """load() handles Unicode keys and values correctly."""
        result = self.adapter.load("città: Roma\n")
        assert result["città"] == "Roma"

    def test_load_empty_string(self):
        """load() returns an empty dict for an empty YAML string."""
        assert self.adapter.load(YAML_EMPTY) == {}

    def test_load_comments_only(self):
        """load() returns an empty dict for YAML containing only comments."""
        assert self.adapter.load(YAML_ONLY_COMMENTS) == {}

    def test_load_invalid_yaml(self):
        """load() raises ValueError for syntactically invalid YAML."""
        with pytest.raises(ValueError, match="Invalid YAML content"):
            self.adapter.load(INVALID_YAML)

    def test_load_scalar_root(self):
        """load() raises ValueError when YAML root is a scalar."""
        with pytest.raises(ValueError, match="root must be a mapping"):
            self.adapter.load(YAML_SCALAR_ROOT)

    def test_load_list_root(self):
        """load() raises ValueError when YAML root is a sequence."""
        with pytest.raises(ValueError, match="root must be a mapping"):
            self.adapter.load("- item1\n- item2\n")


class TestYAMLAdapterDump:
    """Tests for YAMLAdapter.dump()."""

    def setup_method(self):
        self.adapter = YAMLAdapter()

    def test_dump_valid(self):
        """dump() produces valid YAML that parses back to the original dict."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        parsed = yaml.safe_load(raw)
        assert parsed == SAMPLE_NESTED

    def test_dump_block_style(self):
        """dump() uses YAML block style, not flow style."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        assert "{" not in raw  # not flow style

    def test_dump_unicode_preserved(self):
        """dump() preserves Unicode characters in keys and values."""
        raw = self.adapter.dump({"città": "Roma"})
        assert "Roma" in raw
        assert "città" in raw

    def test_dump_empty_dict(self):
        """dump() serializes an empty dict to valid YAML."""
        raw = self.adapter.dump({})
        parsed = yaml.safe_load(raw)
        assert parsed == {} or parsed is None

    def test_dump_round_trip(self):
        """Data survives a dump() → load() round-trip unchanged."""
        raw = self.adapter.dump(SAMPLE_NESTED)
        assert self.adapter.load(raw) == SAMPLE_NESTED

    def test_dump_does_not_sort_keys(self):
        """Keys must preserve insertion order (sort_keys=False)."""
        data = {"zebra": 1, "alpha": 2, "middle": 3}
        raw = self.adapter.dump(data)
        keys_in_output = [
            line.split(":")[0] for line in raw.strip().splitlines() if ":" in line
        ]
        assert keys_in_output == ["zebra", "alpha", "middle"]


# ================================================================== #
# EnvAdapter                                                          #
# ================================================================== #


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


# ================================================================== #
# TOMLAdapter                                                         #
# ================================================================== #


class TestTOMLAdapterLoad:
    """Tests for TOMLAdapter.load()."""

    def setup_method(self):
        self.adapter = TOMLAdapter()

    def test_load_valid(self):
        """load() parses valid TOML and returns the expected nested dict."""
        from sample_data import SAMPLE_TOML

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
        from sample_data import INVALID_TOML

        with pytest.raises(ValueError, match="Invalid TOML content"):
            self.adapter.load(INVALID_TOML)

    def test_load_scalar_root(self):
        """load() raises ValueError when TOML root is a scalar."""
        from sample_data import TOML_SCALAR_ROOT

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
