"""
Tests for ConfigurationManager — optional Singleton + Facade.

Covers:
    - Optional singleton behaviour via instance() (identity, thread safety)
    - load() / merge() / get() / get_all()
    - Dot-notation access with defaults
    - Deep-merge semantics
    - translate() across formats
    - register_creator() extensibility
    - Error paths (unsupported format, not loaded, file not found)
    - reset() / _destroy() housekeeping
"""

import json
import threading
from pathlib import Path

import pytest
import yaml
from sample_data import SAMPLE_NESTED

from proteus.core import ConfigurationManager
from proteus.exceptions import (
    ConfigurationNotLoadedError,
    InvalidKeyError,
    UnsupportedFormatError,
)
from proteus.formats.base_format import FormatCreator
from proteus.readers.base import BaseReader
from proteus.writers.base import BaseWriter

# ------------------------------------------------------------------ #
# Ensure every test gets a fresh singleton                            #
# ------------------------------------------------------------------ #


@pytest.fixture(autouse=True)
def fresh_manager():
    """Destroy and recreate the singleton before each test."""
    ConfigurationManager._destroy()
    yield
    ConfigurationManager._destroy()


# ================================================================== #
# Singleton behaviour                                                 #
# ================================================================== #


class TestSingleton:
    """Verify optional singleton guarantees."""

    def test_constructor_returns_independent_instances(self):
        """Direct construction returns independent objects."""
        a = ConfigurationManager()
        b = ConfigurationManager()
        assert a is not b

    def test_instance_returns_singleton(self):
        """instance() returns the shared singleton object."""
        a = ConfigurationManager.instance()
        b = ConfigurationManager.instance()
        assert a is b

    def test_thread_safety(self):
        """Singleton instances created from multiple threads are identical."""
        instances = []

        def create():
            instances.append(ConfigurationManager.instance())

        threads = [threading.Thread(target=create) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(inst is instances[0] for inst in instances)

    def test_destroy_allows_new_instance(self):
        """_destroy() resets the singleton so a new singleton can be created."""
        first = ConfigurationManager.instance()
        ConfigurationManager._destroy()
        second = ConfigurationManager.instance()
        assert first is not second

    def test_reset_keeps_same_singleton_instance(self):
        """reset() clears state but does not destroy the singleton."""
        mgr = ConfigurationManager.instance()
        mgr.reset()
        assert ConfigurationManager.instance() is mgr


# ================================================================== #
# load() + get()                                                      #
# ================================================================== #


class TestLoadAndGet:
    """Test loading files and accessing values."""

    def test_load_json(self, json_file):
        """load() parses a JSON file and populates the configuration."""
        mgr = ConfigurationManager()
        mgr.load(json_file)

        assert mgr.get("database.host") == "localhost"
        assert mgr.get("database.port") == 5432
        assert mgr.get("app.debug") is True

    def test_load_yaml(self, yaml_file):
        """load() parses a YAML file and populates the configuration."""
        mgr = ConfigurationManager()
        mgr.load(yaml_file)
        assert mgr.get("app.name") == "Proteus"

    def test_load_env(self, tmp_path):
        """load() parses an .env file and populates the configuration."""
        path = tmp_path / "cfg.env"
        path.write_text("DB_HOST=localhost\nDEBUG=true\n", encoding="utf-8")

        mgr = ConfigurationManager()
        mgr.load(str(path))
        assert mgr.get("DB_HOST") == "localhost"

    def test_get_returns_dict(self):
        """get() returns the sub-dict when key points to a branch."""
        mgr = ConfigurationManager()
        mgr._config = SAMPLE_NESTED.copy()
        assert isinstance(mgr.get("database"), dict)

    def test_get_default(self):
        """get() returns the provided default when the key is missing."""
        mgr = ConfigurationManager()
        mgr._config = {"key": "value"}
        assert mgr.get("missing", "fallback") == "fallback"

    def test_get_default_none(self):
        """get() returns None by default when the key is missing."""
        mgr = ConfigurationManager()
        mgr._config = {"key": "value"}
        assert mgr.get("missing") is None

    def test_get_not_loaded_raises(self):
        """get() raises ConfigurationNotLoadedError when no config is loaded."""
        mgr = ConfigurationManager()
        msg = "No configuration loaded"
        with pytest.raises(ConfigurationNotLoadedError, match=msg):
            mgr.get("any.key")

    def test_get_invalid_key_raises(self):
        """get() raises InvalidKeyError for malformed keys."""
        mgr = ConfigurationManager()
        mgr._config = {"a": 1}

        for invalid in ("", " ", ".a", "a.", "a..b"):
            with pytest.raises(InvalidKeyError):
                mgr.get(invalid)

    def test_get_all(self, json_file):
        """get_all() returns a deep copy of the entire configuration."""
        mgr = ConfigurationManager()
        mgr.load(json_file)
        all_cfg = mgr.get_all()
        assert all_cfg == SAMPLE_NESTED
        # Must be a deep copy
        all_cfg["extra"] = True
        assert "extra" not in mgr.get_all()

    def test_get_all_nested_mutation_does_not_leak(self, json_file):
        """Nested mutation on get_all() result does not affect manager state."""
        mgr = ConfigurationManager()
        mgr.load(json_file)
        all_cfg = mgr.get_all()
        all_cfg["database"]["host"] = "HACKED"

        assert mgr.get("database.host") == "localhost"

    def test_loaded_files(self, json_file):
        """loaded_files() returns a list of all files loaded so far."""
        mgr = ConfigurationManager()
        mgr.load(json_file)
        files = mgr.loaded_files()
        assert len(files) == 1
        assert json_file in files[0]


# ================================================================== #
# merge() + deep-merge semantics                                      #
# ================================================================== #


class TestMerge:
    """Test deep-merge behaviour."""

    def test_merge_overrides_scalars(self, tmp_path):
        """merge() overrides scalar values while preserving untouched keys."""
        base = tmp_path / "base.json"
        base.write_text(
            json.dumps({"database": {"host": "localhost", "port": 5432}}),
            encoding="utf-8",
        )
        override = tmp_path / "prod.json"
        override.write_text(
            json.dumps({"database": {"host": "prod-db.example.com"}}),
            encoding="utf-8",
        )

        mgr = ConfigurationManager()
        mgr.load(str(base))
        mgr.merge(str(override))

        assert mgr.get("database.host") == "prod-db.example.com"
        assert mgr.get("database.port") == 5432  # preserved from base

    def test_merge_adds_new_keys(self, tmp_path):
        """merge() adds new top-level keys from the override file."""
        base = tmp_path / "base.json"
        base.write_text(json.dumps({"a": 1}), encoding="utf-8")
        extra = tmp_path / "extra.json"
        extra.write_text(json.dumps({"b": 2}), encoding="utf-8")

        mgr = ConfigurationManager()
        mgr.load(str(base))
        mgr.merge(str(extra))

        assert mgr.get("a") == 1
        assert mgr.get("b") == 2

    def test_deep_merge_recursive(self):
        """Static _deep_merge works correctly on nested dicts."""
        base = {"x": {"y": {"z": 1, "w": 2}}}
        over = {"x": {"y": {"z": 99}}}
        result = ConfigurationManager._deep_merge(base, over)
        assert result == {"x": {"y": {"z": 99, "w": 2}}}

    def test_deep_merge_does_not_mutate(self):
        """_deep_merge() does not mutate the original base dict."""
        base = {"a": {"b": 1}}
        over = {"a": {"b": 2}}
        ConfigurationManager._deep_merge(base, over)
        assert base == {"a": {"b": 1}}


# ================================================================== #
# translate()                                                         #
# ================================================================== #


class TestTranslate:
    """Test format translation through the Facade."""

    def test_json_to_yaml(self, json_file, yaml_output):
        """translate() converts a JSON file to YAML format."""
        mgr = ConfigurationManager()
        mgr.translate(json_file, str(yaml_output))

        assert yaml.safe_load(yaml_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    def test_yaml_to_json(self, yaml_file, json_output):
        """translate() converts a YAML file to JSON format."""
        mgr = ConfigurationManager()
        mgr.translate(yaml_file, str(json_output))

        assert json.loads(json_output.read_text(encoding="utf-8")) == SAMPLE_NESTED

    def test_json_to_env(self, tmp_path):
        """translate() converts a flat JSON file to .env format."""
        flat = {"host": "localhost", "port": 8080}
        src = tmp_path / "flat.json"
        src.write_text(json.dumps(flat), encoding="utf-8")
        dst = str(tmp_path / "output.env")

        mgr = ConfigurationManager()
        mgr.translate(str(src), dst)

        content = (tmp_path / "output.env").read_text(encoding="utf-8")
        assert "HOST=localhost" in content
        assert "PORT=8080" in content

    def test_translate_unsupported_input(self, tmp_path):
        """translate() raises UnsupportedFormatError for unknown input formats."""
        src = tmp_path / "source.xml"
        src.write_text("<xml/>", encoding="utf-8")
        dst = str(tmp_path / "output.json")

        mgr = ConfigurationManager()
        with pytest.raises(UnsupportedFormatError, match="not supported"):
            mgr.translate(str(src), dst)

    def test_translate_unsupported_output(self, json_file, tmp_path):
        """translate() raises UnsupportedFormatError for unknown output formats."""
        dst = str(tmp_path / "output.xml")

        mgr = ConfigurationManager()
        with pytest.raises(UnsupportedFormatError, match="not supported"):
            mgr.translate(json_file, dst)

    def test_translate_file_not_found(self, tmp_path):
        """translate() raises FileNotFoundError for a nonexistent source file."""
        dst = str(tmp_path / "output.json")

        mgr = ConfigurationManager()
        with pytest.raises(FileNotFoundError):
            mgr.translate(str(tmp_path / "ghost.yaml"), dst)

    def test_translate_accepts_path_objects(self, json_file, tmp_path):
        """translate() accepts pathlib.Path objects for both paths."""
        src = Path(json_file)
        dst = tmp_path / "output.yaml"

        mgr = ConfigurationManager()
        mgr.translate(src, dst)

        assert dst.exists()

    def test_translate_and_load_accepts_path_objects(self, json_file, tmp_path):
        """translate_and_load() accepts pathlib.Path objects for both paths."""
        src = Path(json_file)
        dst = tmp_path / "output.yaml"

        mgr = ConfigurationManager()
        mgr.translate_and_load(src, dst)

        assert dst.exists()
        assert mgr.get("database.host") == "localhost"

    def test_translate_and_load_updates_state(self, json_file, tmp_path):
        """translate_and_load() writes output and updates state."""
        output = tmp_path / "translated.yaml"

        mgr = ConfigurationManager()
        mgr.translate_and_load(json_file, str(output))

        assert output.exists()
        assert mgr.get("database.host") == "localhost"
        assert len(mgr.loaded_files()) == 1
        assert str(output.resolve()) in mgr.loaded_files()[0]


# ================================================================== #
# Context manager                                                     #
# ================================================================== #


class TestContextManager:
    """Verify the manager can be used as a context manager."""

    def test_temporary_context_resets_state(self, json_file):
        with ConfigurationManager.temporary() as mgr:
            mgr.load(json_file)
            assert mgr.get("database.host") == "localhost"
            assert mgr.loaded_files()

        assert mgr.get_all() == {}
        assert mgr.loaded_files() == []

    def test_temporary_accepts_path_objects(self, json_file):
        with ConfigurationManager.temporary() as mgr:
            mgr.load(Path(json_file))
            assert mgr.get("database.host") == "localhost"


# ================================================================== #
# Unsupported format                                                  #
# ================================================================== #


class TestUnsupportedFormat:
    """Verify error handling for unsupported file formats."""

    def test_load_unsupported(self, tmp_path):
        """load() raises UnsupportedFormatError for an unknown extension."""
        path = tmp_path / "cfg.xml"
        path.write_text("<xml/>", encoding="utf-8")

        mgr = ConfigurationManager()
        with pytest.raises(UnsupportedFormatError, match="not supported"):
            mgr.load(str(path))

    def test_error_lists_available(self, tmp_path):
        """The UnsupportedFormatError message lists available formats."""
        path = tmp_path / "cfg.toml"
        path.write_text("", encoding="utf-8")

        mgr = ConfigurationManager()
        with pytest.raises(UnsupportedFormatError, match=r"\.json"):
            mgr.load(str(path))


# ================================================================== #
# register_creator() extensibility                                    #
# ================================================================== #


class TestRegisterCreator:
    """Verify that custom creators can be plugged in."""

    def _make_dummy_creator(self):
        """Create a minimal FormatCreator for .dummy extension."""

        class DummyReader(BaseReader):
            def _parse_content(self, raw):
                return {"dummy": raw.strip()}

        class DummyWriter(BaseWriter):
            def _serialize(self, data):
                return str(data)

        class DummyCreator(FormatCreator):
            def create_reader(self):
                return DummyReader()

            def create_writer(self):
                return DummyWriter()

            def get_extensions(self):
                return [".dummy"]

        return DummyCreator()

    def test_register_and_load(self, tmp_path):
        """A registered custom creator can load its format."""
        path = tmp_path / "test.dummy"
        path.write_text("hello", encoding="utf-8")

        mgr = ConfigurationManager()
        mgr.register_creator(self._make_dummy_creator())
        mgr.load(str(path))
        assert mgr.get("dummy") == "hello"

    def test_register_overrides_existing(self):
        """Registering a creator for an existing extension replaces it."""
        mgr = ConfigurationManager()
        original = mgr._creators.get(".json")

        class AltJSONCreator(FormatCreator):
            def create_reader(self):
                return original.create_reader()

            def create_writer(self):
                return original.create_writer()

            def get_extensions(self):
                return [".json"]

        alt = AltJSONCreator()
        mgr.register_creator(alt)
        assert mgr._creators[".json"] is alt


# ================================================================== #
# reset()                                                             #
# ================================================================== #


class TestReset:
    """Verify reset() clears state without destroying the singleton."""

    def test_reset_clears_config(self, json_file):
        """reset() removes all loaded configuration data."""
        mgr = ConfigurationManager()
        mgr.load(json_file)
        assert mgr.get_all() != {}

        mgr.reset()
        assert mgr.get_all() == {}

    def test_reset_clears_loaded_files(self, json_file):
        """reset() empties the loaded_files() list."""
        mgr = ConfigurationManager()
        mgr.load(json_file)
        assert len(mgr.loaded_files()) == 1

        mgr.reset()
        assert mgr.loaded_files() == []


# ================================================================== #
# Default creators registered                                         #
# ================================================================== #


class TestDefaultCreators:
    """Verify that all built-in formats are registered out of the box."""

    def test_json_registered(self):
        """The .json extension is registered by default."""
        mgr = ConfigurationManager()
        assert ".json" in mgr._creators

    def test_yaml_registered(self):
        """Both .yaml and .yml extensions are registered by default."""
        mgr = ConfigurationManager()
        assert ".yaml" in mgr._creators
        assert ".yml" in mgr._creators

    def test_env_registered(self):
        """The .env extension is registered by default."""
        mgr = ConfigurationManager()
        assert ".env" in mgr._creators


# ================================================================== #
# Package-level import                                                #
# ================================================================== #


class TestPackageImport:
    """Verify that ConfigurationManager is importable from the top-level package."""

    def test_import_from_package(self):
        """ConfigurationManager is accessible via `from proteus import ...`."""
        from proteus import ConfigurationManager

        assert ConfigurationManager is not None
