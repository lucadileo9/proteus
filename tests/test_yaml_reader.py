"""
Tests for YAMLReader — Template Method concrete participant.

Covers:
    - Successful parsing of valid YAML files
    - Edge cases (empty file, comments-only, scalar root)
    - Template Method validation steps
    - Delegation to YAMLAdapter
"""

import pytest
from proteus.readers.yaml_reader import YAMLReader
from sample_data import (
    SAMPLE_NESTED,
    SAMPLE_YAML,
    INVALID_YAML,
    YAML_EMPTY,
    YAML_ONLY_COMMENTS,
    YAML_SCALAR_ROOT,
)


class TestYAMLReaderParse:
    """Test the Template Method parse() flow for YAML."""

    def setup_method(self):
        self.reader = YAMLReader()

    # ------------------------------------------------------------------ #
    # Happy path                                                          #
    # ------------------------------------------------------------------ #

    def test_parse_valid_yaml(self, yaml_file):
        """parse() returns the expected Dict IR from a valid YAML file."""
        result = self.reader.parse(yaml_file)
        assert result == SAMPLE_NESTED

    def test_parse_returns_dict(self, yaml_file):
        """parse() always returns a dict."""
        result = self.reader.parse(yaml_file)
        assert isinstance(result, dict)

    def test_parse_preserves_types(self, yaml_file):
        """Numeric and boolean values are preserved through parsing."""
        result = self.reader.parse(yaml_file)
        assert result["database"]["port"] == 5432
        assert isinstance(result["database"]["port"], int)
        assert result["app"]["debug"] is True

    def test_parse_nested_access(self, yaml_file):
        """Nested keys are accessible via regular dict traversal."""
        result = self.reader.parse(yaml_file)
        assert result["database"]["host"] == "localhost"
        assert result["app"]["name"] == "Proteus"

    def test_parse_unicode(self, tmp_path):
        """parse() handles Unicode content correctly."""
        path = tmp_path / "unicode.yaml"
        path.write_text("città: Roma\n名前: 太郎\n", encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["città"] == "Roma"
        assert result["名前"] == "太郎"

    # ------------------------------------------------------------------ #
    # Edge cases                                                          #
    # ------------------------------------------------------------------ #

    def test_parse_empty_file(self, tmp_path):
        """parse() returns empty dict for an empty YAML file."""
        path = tmp_path / "empty.yaml"
        path.write_text(YAML_EMPTY, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {}

    def test_parse_comments_only(self, tmp_path):
        """parse() returns empty dict for a YAML file with only comments."""
        path = tmp_path / "comments.yaml"
        path.write_text(YAML_ONLY_COMMENTS, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {}

    def test_parse_minimal_yaml(self, tmp_path):
        """parse() handles a minimal one-key YAML."""
        path = tmp_path / "minimal.yaml"
        path.write_text("key: value\n", encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == {"key": "value"}

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_parse_file_not_found(self, tmp_path):
        """parse() raises FileNotFoundError for a nonexistent file."""
        fake = str(tmp_path / "nonexistent.yaml")
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.reader.parse(fake)

    def test_parse_not_a_file(self, tmp_path):
        """parse() raises ValueError when path is a directory."""
        with pytest.raises(ValueError, match="Not a regular file"):
            self.reader.parse(str(tmp_path))

    # ------------------------------------------------------------------ #
    # Adapter-level errors                                                #
    # ------------------------------------------------------------------ #

    def test_parse_invalid_yaml(self, tmp_path):
        """parse() raises ValueError for syntactically invalid YAML."""
        path = tmp_path / "invalid.yaml"
        path.write_text(INVALID_YAML, encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid YAML content"):
            self.reader.parse(str(path))

    def test_parse_scalar_root(self, tmp_path):
        """parse() raises ValueError when YAML root is a scalar."""
        path = tmp_path / "scalar.yaml"
        path.write_text(YAML_SCALAR_ROOT, encoding="utf-8")
        with pytest.raises(ValueError, match="root must be a mapping"):
            self.reader.parse(str(path))

    def test_parse_list_root(self, tmp_path):
        """parse() raises ValueError when YAML root is a list."""
        path = tmp_path / "list.yaml"
        path.write_text("- item1\n- item2\n", encoding="utf-8")
        with pytest.raises(ValueError, match="root must be a mapping"):
            self.reader.parse(str(path))


class TestYAMLReaderStructure:
    """Verify structural properties of YAMLReader."""

    def test_has_adapter(self):
        """YAMLReader has a _adapter attribute."""
        reader = YAMLReader()
        assert hasattr(reader, "_adapter")

    def test_adapter_type(self):
        """The adapter is a YAMLAdapter instance."""
        from proteus.adapters.yaml_adapter import YAMLAdapter
        reader = YAMLReader()
        assert isinstance(reader._adapter, YAMLAdapter)
