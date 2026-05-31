"""
Tests for the Format Creator Layer — Factory Method (GoF canonical).

Covers:
    - FormatCreator cannot be instantiated (abstract)
    - Each concrete creator returns the correct reader/writer types
    - Created readers actually parse files (integration)
    - Created writers actually write files (integration)
    - Full round-trip translate workflow via factory-created pairs
    - get_extensions() returns the expected values
    - Cross-format translation through two different creators
"""

import json

import pytest
import yaml
from sample_data import SAMPLE_FLAT, SAMPLE_NESTED

from proteus.adapters.env_adapter import EnvAdapter
from proteus.adapters.json_adapter import JSONAdapter
from proteus.adapters.yaml_adapter import YAMLAdapter
from proteus.formats.base_format import FormatCreator
from proteus.formats.env_format import EnvFormatCreator
from proteus.formats.json_format import JSONFormatCreator
from proteus.formats.yaml_format import YAMLFormatCreator
from proteus.readers.base import BaseReader
from proteus.readers.env_reader import EnvReader
from proteus.readers.json_reader import JSONReader
from proteus.readers.yaml_reader import YAMLReader
from proteus.writers.base import BaseWriter
from proteus.writers.env_writer import EnvWriter
from proteus.writers.json_writer import JSONWriter
from proteus.writers.yaml_writer import YAMLWriter

# ================================================================== #
# FormatCreator — abstract base                                       #
# ================================================================== #


class TestFormatCreatorAbstract:
    """Verify that FormatCreator cannot be instantiated directly."""

    def test_cannot_instantiate(self):
        """FormatCreator is abstract and raises TypeError."""
        with pytest.raises(TypeError):
            FormatCreator()

    def test_is_abstract(self):
        """FormatCreator has the expected abstract methods."""
        abstracts = FormatCreator.__abstractmethods__
        assert "create_reader" in abstracts
        assert "create_writer" in abstracts
        assert "get_extensions" in abstracts

    def test_subclass_must_implement_all(self):
        """A subclass missing any factory method is still abstract."""

        class IncompleteCreator(FormatCreator):
            def create_reader(self):
                return None

            # missing create_writer and get_extensions

        with pytest.raises(TypeError):
            IncompleteCreator()


# ================================================================== #
# JSONFormatCreator                                                   #
# ================================================================== #


class TestJSONFormatCreator:
    """Tests for the JSON concrete creator."""

    def setup_method(self):
        self.creator = JSONFormatCreator()

    # -- Factory Method contracts ----------------------------------- #

    def test_create_reader_returns_json_reader(self):
        """create_reader() returns a JSONReader instance."""
        reader = self.creator.create_reader()
        assert isinstance(reader, JSONReader)

    def test_create_reader_is_base_reader(self):
        """The created reader is a BaseReader subclass."""
        reader = self.creator.create_reader()
        assert isinstance(reader, BaseReader)

    def test_create_writer_returns_json_writer(self):
        """create_writer() returns a JSONWriter instance."""
        writer = self.creator.create_writer()
        assert isinstance(writer, JSONWriter)

    def test_create_writer_is_base_writer(self):
        """The created writer is a BaseWriter subclass."""
        writer = self.creator.create_writer()
        assert isinstance(writer, BaseWriter)

    def test_reader_has_json_adapter(self):
        """The created reader uses a JSONAdapter internally."""
        reader = self.creator.create_reader()
        assert isinstance(reader._adapter, JSONAdapter)

    def test_reader_and_writer_share_adapter(self):
        """Reader and writer created by the same creator share one adapter instance."""
        reader = self.creator.create_reader()
        writer = self.creator.create_writer()
        assert reader._adapter is writer._adapter

    def test_writer_has_json_adapter(self):
        """The created writer uses a JSONAdapter internally."""
        writer = self.creator.create_writer()
        assert isinstance(writer._adapter, JSONAdapter)

    def test_get_extensions(self):
        """get_extensions() returns ['.json']."""
        assert self.creator.get_extensions() == [".json"]

    def test_creates_new_instances(self):
        """Each call returns a fresh instance (no shared state)."""
        r1 = self.creator.create_reader()
        r2 = self.creator.create_reader()
        assert r1 is not r2

        w1 = self.creator.create_writer()
        w2 = self.creator.create_writer()
        assert w1 is not w2

    # -- Integration: reader actually works ------------------------- #

    def test_reader_parses_json(self, json_file):
        """Reader created by the factory parses a JSON file correctly."""
        reader = self.creator.create_reader()
        result = reader.parse(json_file)
        assert result == SAMPLE_NESTED

    # -- Integration: writer actually works ------------------------- #

    def test_writer_writes_json(self, json_output):
        """Writer created by the factory writes a valid JSON file."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_NESTED, str(json_output))

        assert json.loads(json_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    # -- Integration: round-trip via factory ------------------------ #

    def test_round_trip(self, json_output):
        """Data survives write → read round-trip through factory pair."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_NESTED, str(json_output))

        reader = self.creator.create_reader()
        assert reader.parse(str(json_output)) == SAMPLE_NESTED


# ================================================================== #
# YAMLFormatCreator                                                   #
# ================================================================== #


class TestYAMLFormatCreator:
    """Tests for the YAML concrete creator."""

    def setup_method(self):
        self.creator = YAMLFormatCreator()

    # -- Factory Method contracts ----------------------------------- #

    def test_create_reader_returns_yaml_reader(self):
        """create_reader() returns a YAMLReader instance."""
        reader = self.creator.create_reader()
        assert isinstance(reader, YAMLReader)

    def test_create_reader_is_base_reader(self):
        """The created reader is a BaseReader subclass."""
        reader = self.creator.create_reader()
        assert isinstance(reader, BaseReader)

    def test_create_writer_returns_yaml_writer(self):
        """create_writer() returns a YAMLWriter instance."""
        writer = self.creator.create_writer()
        assert isinstance(writer, YAMLWriter)

    def test_create_writer_is_base_writer(self):
        """The created writer is a BaseWriter subclass."""
        writer = self.creator.create_writer()
        assert isinstance(writer, BaseWriter)

    def test_reader_has_yaml_adapter(self):
        """The created reader uses a YAMLAdapter internally."""
        reader = self.creator.create_reader()
        assert isinstance(reader._adapter, YAMLAdapter)

    def test_reader_and_writer_share_adapter(self):
        """Reader and writer created by the same creator share one adapter instance."""
        reader = self.creator.create_reader()
        writer = self.creator.create_writer()
        assert reader._adapter is writer._adapter

    def test_writer_has_yaml_adapter(self):
        """The created writer uses a YAMLAdapter internally."""
        writer = self.creator.create_writer()
        assert isinstance(writer._adapter, YAMLAdapter)

    def test_get_extensions(self):
        """YAML supports both .yaml and .yml."""
        exts = self.creator.get_extensions()
        assert ".yaml" in exts
        assert ".yml" in exts

    def test_creates_new_instances(self):
        """Each call returns a fresh instance (no shared state)."""
        r1 = self.creator.create_reader()
        r2 = self.creator.create_reader()
        assert r1 is not r2

    # -- Integration ------------------------------------------------ #

    def test_reader_parses_yaml(self, yaml_file):
        """Reader created by the factory parses a YAML file correctly."""
        reader = self.creator.create_reader()
        result = reader.parse(yaml_file)
        assert result == SAMPLE_NESTED

    def test_writer_writes_yaml(self, yaml_output):
        """Writer created by the factory writes a valid YAML file."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_NESTED, str(yaml_output))

        assert yaml.safe_load(yaml_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    def test_round_trip(self, yaml_output):
        """Data survives write → read round-trip through factory pair."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_NESTED, str(yaml_output))

        reader = self.creator.create_reader()
        assert reader.parse(str(yaml_output)) == SAMPLE_NESTED


# ================================================================== #
# EnvFormatCreator                                                    #
# ================================================================== #


class TestEnvFormatCreator:
    """Tests for the ENV concrete creator."""

    def setup_method(self):
        self.creator = EnvFormatCreator()

    # -- Factory Method contracts ----------------------------------- #

    def test_create_reader_returns_env_reader(self):
        """create_reader() returns an EnvReader instance."""
        reader = self.creator.create_reader()
        assert isinstance(reader, EnvReader)

    def test_create_reader_is_base_reader(self):
        """The created reader is a BaseReader subclass."""
        reader = self.creator.create_reader()
        assert isinstance(reader, BaseReader)

    def test_create_writer_returns_env_writer(self):
        """create_writer() returns an EnvWriter instance."""
        writer = self.creator.create_writer()
        assert isinstance(writer, EnvWriter)

    def test_create_writer_is_base_writer(self):
        """The created writer is a BaseWriter subclass."""
        writer = self.creator.create_writer()
        assert isinstance(writer, BaseWriter)

    def test_reader_has_env_adapter(self):
        """The created reader uses an EnvAdapter internally."""
        reader = self.creator.create_reader()
        assert isinstance(reader._adapter, EnvAdapter)

    def test_reader_and_writer_share_adapter(self):
        """Reader and writer created by the same creator share one adapter instance."""
        reader = self.creator.create_reader()
        writer = self.creator.create_writer()
        assert reader._adapter is writer._adapter

    def test_writer_has_env_adapter(self):
        """The created writer uses an EnvAdapter internally."""
        writer = self.creator.create_writer()
        assert isinstance(writer._adapter, EnvAdapter)

    def test_get_extensions(self):
        """get_extensions() returns ['.env']."""
        assert self.creator.get_extensions() == [".env"]

    def test_creates_new_instances(self):
        """Each call returns a fresh instance (no shared state)."""
        r1 = self.creator.create_reader()
        r2 = self.creator.create_reader()
        assert r1 is not r2

    # -- Integration ------------------------------------------------ #

    def test_reader_parses_env(self, env_file):
        """Reader created by the factory parses an .env file correctly."""
        reader = self.creator.create_reader()
        result = reader.parse(env_file)
        assert result == SAMPLE_FLAT

    def test_writer_writes_env(self, env_output):
        """Writer created by the factory writes a valid .env file."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_FLAT, str(env_output))

        content = env_output.read_text(encoding="utf-8")
        for key in SAMPLE_FLAT:
            assert key.upper() in content

    def test_round_trip_flat(self, env_output):
        """Flat data survives write → read round-trip."""
        writer = self.creator.create_writer()
        writer.write(SAMPLE_FLAT, str(env_output))

        reader = self.creator.create_reader()
        assert reader.parse(str(env_output)) == SAMPLE_FLAT


# ================================================================== #
# Cross-format translation (the raison d'être of Factory Method)      #
# ================================================================== #


class TestCrossFormatTranslation:
    """
    Simulate the translate() workflow using two different creators.

    This is the core scenario Factory Method was designed for:
    CreatorA.create_reader() reads format A  →  Dict (IR)
    CreatorB.create_writer() writes format B  →  file
    """

    def test_json_to_yaml(self, json_file, yaml_output):
        """Translate JSON → YAML through factory-created pairs."""
        reader = JSONFormatCreator().create_reader()
        writer = YAMLFormatCreator().create_writer()

        data = reader.parse(json_file)
        writer.write(data, str(yaml_output))

        assert yaml.safe_load(yaml_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    def test_yaml_to_json(self, yaml_file, json_output):
        """Translate YAML → JSON through factory-created pairs."""
        reader = YAMLFormatCreator().create_reader()
        writer = JSONFormatCreator().create_writer()

        data = reader.parse(yaml_file)
        writer.write(data, str(json_output))

        assert json.loads(json_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    def test_json_to_env(self, json_file, env_output):
        """Translate JSON (nested) → ENV through factory-created pairs."""
        reader = JSONFormatCreator().create_reader()
        writer = EnvFormatCreator().create_writer()

        data = reader.parse(json_file)
        writer.write(data, str(env_output))

        content = env_output.read_text(encoding="utf-8")
        assert "DATABASE__HOST=localhost" in content
        assert "DATABASE__PORT=5432" in content
        assert "APP__NAME=Proteus" in content

    def test_env_to_json(self, env_file, json_output):
        """Translate ENV → JSON through factory-created pairs."""
        reader = EnvFormatCreator().create_reader()
        writer = JSONFormatCreator().create_writer()

        data = reader.parse(env_file)
        writer.write(data, str(json_output))

        assert json.loads(json_output.read_text(encoding="utf-8")) == SAMPLE_FLAT

    def test_yaml_to_env(self, yaml_file, env_output):
        """Translate YAML (nested) → ENV through factory-created pairs."""
        reader = YAMLFormatCreator().create_reader()
        writer = EnvFormatCreator().create_writer()

        data = reader.parse(yaml_file)
        writer.write(data, str(env_output))

        content = env_output.read_text(encoding="utf-8")
        assert "DATABASE__HOST=localhost" in content
        assert "DATABASE__PORT=5432" in content
        assert "APP__NAME=Proteus" in content


# ================================================================== #
# Package-level imports                                               #
# ================================================================== #


class TestFormatsPackageImports:
    """Verify public API accessible through the package __init__."""

    def test_import_format_creator(self):
        """FormatCreator is importable from the formats package."""
        from proteus.formats import FormatCreator

        assert FormatCreator is not None

    def test_import_json_format_creator(self):
        """JSONFormatCreator is importable from the formats package."""
        from proteus.formats import JSONFormatCreator

        assert JSONFormatCreator is not None

    def test_import_yaml_format_creator(self):
        """YAMLFormatCreator is importable from the formats package."""
        from proteus.formats import YAMLFormatCreator

        assert YAMLFormatCreator is not None

    def test_import_env_format_creator(self):
        """EnvFormatCreator is importable from the formats package."""
        from proteus.formats import EnvFormatCreator

        assert EnvFormatCreator is not None
