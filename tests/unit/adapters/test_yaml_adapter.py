import pytest
import yaml
from sample_data import (
    INVALID_YAML,
    SAMPLE_NESTED,
    SAMPLE_YAML,
    YAML_EMPTY,
    YAML_ONLY_COMMENTS,
    YAML_SCALAR_ROOT,
)

from proteus.adapters.yaml_adapter import YAMLAdapter


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
