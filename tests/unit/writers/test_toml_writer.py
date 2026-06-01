import pytest
from sample_data import SAMPLE_NESTED

from proteus.readers.toml_reader import TOMLReader
from proteus.writers.toml_writer import TOMLWriter


class TestTOMLWriterWrite:
    """Test the Template Method write() flow for TOML."""

    def setup_method(self):
        self.writer = TOMLWriter()

    def test_write_creates_file(self, tmp_path):
        """write() creates a file at the specified path."""
        path = str(tmp_path / "output.toml")
        self.writer.write(SAMPLE_NESTED, path)
        assert (tmp_path / "output.toml").exists()

    def test_write_valid_toml_output(self, tmp_path):
        """The written file contains valid TOML."""
        path = str(tmp_path / "output.toml")
        self.writer.write(SAMPLE_NESTED, path)
        # Use reader to verify the content
        result = TOMLReader().parse(path)
        assert result == SAMPLE_NESTED

    def test_round_trip(self, tmp_path):
        """Data survives a write → read round-trip unchanged."""
        path = str(tmp_path / "roundtrip.toml")
        self.writer.write(SAMPLE_NESTED, path)
        result = TOMLReader().parse(path)
        assert result == SAMPLE_NESTED

    def test_write_non_dict_raises_type_error(self, tmp_path):
        """write() raises TypeError if data is not a dict."""
        path = str(tmp_path / "output.toml")
        with pytest.raises(TypeError, match="data must be a dict"):
            self.writer.write("not a dict", path)  # type: ignore[arg-type]


class TestTOMLWriterStructure:
    """Verify structural properties of TOMLWriter."""

    def test_has_adapter(self):
        """TOMLWriter has a _adapter attribute."""
        writer = TOMLWriter()
        assert hasattr(writer, "_adapter")

    def test_adapter_type(self):
        """The adapter is a TOMLAdapter instance."""
        from proteus.adapters.toml_adapter import TOMLAdapter

        writer = TOMLWriter()
        assert isinstance(writer._adapter, TOMLAdapter)
