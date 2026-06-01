"""
Tests for YAMLWriter — Template Method concrete participant.

Covers:
    - Successful writing of valid data
    - Output format correctness (valid YAML, block style, unicode)
    - Template Method validation steps
    - Round-trip consistency with YAMLReader
"""

import pytest
import yaml
from sample_data import SAMPLE_NESTED

from proteus.readers.yaml_reader import YAMLReader
from proteus.writers.yaml_writer import YAMLWriter


class TestYAMLWriterWrite:
    """Test the Template Method write() flow for YAML."""

    def setup_method(self):
        self.writer = YAMLWriter()

    # ------------------------------------------------------------------ #
    # Happy path                                                          #
    # ------------------------------------------------------------------ #

    def test_write_creates_file(self, tmp_path):
        """write() creates a file at the specified path."""
        path = str(tmp_path / "output.yaml")
        self.writer.write(SAMPLE_NESTED, path)
        assert (tmp_path / "output.yaml").exists()

    def test_write_valid_yaml_output(self, tmp_path):
        """The written file contains valid YAML."""
        path = str(tmp_path / "output.yaml")
        self.writer.write(SAMPLE_NESTED, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed == SAMPLE_NESTED

    def test_write_preserves_types(self, tmp_path):
        """Numeric and boolean values are preserved in the output."""
        path = str(tmp_path / "output.yaml")
        self.writer.write(SAMPLE_NESTED, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed["database"]["port"] == 5432
        assert parsed["app"]["debug"] is True

    def test_write_block_style(self, tmp_path):
        """Output uses block style (not flow/inline)."""
        path = str(tmp_path / "output.yaml")
        self.writer.write(SAMPLE_NESTED, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        # Block style means we should see indented lines, not {braces}
        assert "{" not in content
        assert "host:" in content or "host :" in content

    def test_write_unicode(self, tmp_path):
        """Unicode characters are preserved."""
        path = str(tmp_path / "output.yaml")
        data = {"città": "Roma", "名前": "太郎"}
        self.writer.write(data, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        assert "Roma" in content
        assert "太郎" in content

    def test_write_empty_dict(self, tmp_path):
        """write() handles an empty dict."""
        path = str(tmp_path / "output.yaml")
        self.writer.write({}, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed == {} or parsed is None  # YAML may dump "{}" or empty

    def test_write_overwrites_existing(self, tmp_path):
        """write() overwrites an existing file."""
        path = str(tmp_path / "output.yaml")
        self.writer.write({"old": "data"}, path)
        self.writer.write({"new": "data"}, path)
        content = (tmp_path / "output.yaml").read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed == {"new": "data"}

    # ------------------------------------------------------------------ #
    # Round-trip with YAMLReader                                          #
    # ------------------------------------------------------------------ #

    def test_round_trip(self, tmp_path):
        """Data survives a write → read round-trip unchanged."""
        path = str(tmp_path / "roundtrip.yaml")
        self.writer.write(SAMPLE_NESTED, path)
        result = YAMLReader().parse(path)
        assert result == SAMPLE_NESTED

    # ------------------------------------------------------------------ #
    # Template Method — _validate() errors                                #
    # ------------------------------------------------------------------ #

    def test_write_non_dict_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is not a dict."""
        path = str(tmp_path / "output.yaml")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write("not a dict", path)

    def test_write_list_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is a list."""
        path = str(tmp_path / "output.yaml")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write([1, 2, 3], path)

    def test_write_none_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is None."""
        path = str(tmp_path / "output.yaml")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write(None, path)

    def test_write_missing_directory(self, tmp_path):
        """write() raises FileNotFoundError if parent dir does not exist."""
        path = str(tmp_path / "nonexistent_dir" / "output.yaml")
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            self.writer.write(SAMPLE_NESTED, path)


class TestYAMLWriterStructure:
    """Verify structural properties of YAMLWriter."""

    def test_has_adapter(self):
        """YAMLWriter has a _adapter attribute."""
        writer = YAMLWriter()
        assert hasattr(writer, "_adapter")

    def test_adapter_type(self):
        """The adapter is a YAMLAdapter instance."""
        from proteus.adapters.yaml_adapter import YAMLAdapter

        writer = YAMLWriter()
        assert isinstance(writer._adapter, YAMLAdapter)
