from pathlib import Path

import pytest
from sample_data import INVALID_TOML, SAMPLE_NESTED, SAMPLE_TOML

from proteus.readers.toml_reader import TOMLReader


class TestTOMLReaderParse:
    """Test the Template Method parse() flow for TOML."""

    def setup_method(self) -> None:
        self.reader = TOMLReader()

    def test_parse_valid_toml(self, tmp_path: Path) -> None:
        """parse() successfully reads a valid TOML file."""
        path = tmp_path / "config.toml"
        path.write_text(SAMPLE_TOML, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result == SAMPLE_NESTED

    def test_parse_returns_dict(self, tmp_path: Path) -> None:
        """The result of parse() is always a dictionary."""
        path = tmp_path / "config.toml"
        path.write_text(SAMPLE_TOML, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert isinstance(result, dict)

    def test_parse_preserves_types(self, tmp_path: Path) -> None:
        """Numeric and boolean values are preserved."""
        path = tmp_path / "config.toml"
        path.write_text(SAMPLE_TOML, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert isinstance(result["database"]["port"], int)
        assert isinstance(result["app"]["debug"], bool)

    def test_parse_nested_access(self, tmp_path: Path) -> None:
        """Deeply nested keys are accessible."""
        path = tmp_path / "config.toml"
        path.write_text(SAMPLE_TOML, encoding="utf-8")
        result = self.reader.parse(str(path))
        assert result["database"]["host"] == "localhost"

    def test_parse_file_not_found(self) -> None:
        """parse() raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            self.reader.parse("nonexistent.toml")

    def test_parse_invalid_toml(self, tmp_path: Path) -> None:
        """parse() raises ValueError for malformed TOML."""
        path = tmp_path / "invalid.toml"
        path.write_text(INVALID_TOML, encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid TOML content"):
            self.reader.parse(str(path))


class TestTOMLReaderStructure:
    """Verify structural properties of TOMLReader."""

    def test_has_adapter(self) -> None:
        """TOMLReader has a _adapter attribute."""
        reader = TOMLReader()
        assert hasattr(reader, "_adapter")

    def test_adapter_type(self) -> None:
        """The adapter is a TOMLAdapter instance."""
        from proteus.adapters.toml_adapter import TOMLAdapter

        reader = TOMLReader()
        assert isinstance(reader._adapter, TOMLAdapter)
