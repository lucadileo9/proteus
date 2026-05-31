"""
Tests for optional adapter dependency injection in readers and writers.

Covers:
    - Readers can receive a custom adapter instance
    - Writers can receive a custom adapter instance
    - Default behavior still uses the built-in adapters when none is provided
"""

from typing import Any, Dict, Optional

from proteus.adapters.base import BaseAdapter
from proteus.readers.env_reader import EnvReader
from proteus.readers.json_reader import JSONReader
from proteus.readers.yaml_reader import YAMLReader
from proteus.writers.env_writer import EnvWriter
from proteus.writers.json_writer import JSONWriter
from proteus.writers.yaml_writer import YAMLWriter


class RecordingAdapter(BaseAdapter):
    def __init__(
        self,
        load_result: Optional[Dict[str, Any]] = None,
        dump_result: str = "",
    ) -> None:
        self.load_result = load_result or {"injected": True}
        self.dump_result = dump_result or "INJECTED=true\n"
        self.last_raw: Optional[str] = None
        self.last_data: Optional[Dict[str, Any]] = None

    def load(self, raw: str) -> Dict[str, Any]:
        self.last_raw = raw
        return self.load_result

    def dump(self, data: Dict[str, Any]) -> str:
        self.last_data = data
        return self.dump_result


class TestReaderDependencyInjection:
    def test_json_reader_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(load_result={"source": "json"})
        path = tmp_path / "config.json"
        path.write_text("raw json content", encoding="utf-8")

        reader = JSONReader(adapter=adapter)
        result = reader.parse(str(path))

        assert result == {"source": "json"}
        assert adapter.last_raw == "raw json content"

    def test_yaml_reader_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(load_result={"source": "yaml"})
        path = tmp_path / "config.yaml"
        path.write_text("raw yaml content", encoding="utf-8")

        reader = YAMLReader(adapter=adapter)
        result = reader.parse(str(path))

        assert result == {"source": "yaml"}
        assert adapter.last_raw == "raw yaml content"

    def test_env_reader_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(load_result={"source": "env"})
        path = tmp_path / ".env"
        path.write_text("raw env content", encoding="utf-8")

        reader = EnvReader(adapter=adapter)
        result = reader.parse(str(path))

        assert result == {"source": "env"}
        assert adapter.last_raw == "raw env content"


class TestWriterDependencyInjection:
    def test_json_writer_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(dump_result='{"injected": true}')
        path = tmp_path / "output.json"

        writer = JSONWriter(adapter=adapter)
        writer.write({"hello": "world"}, str(path))

        assert path.read_text(encoding="utf-8") == '{"injected": true}'
        assert adapter.last_data == {"hello": "world"}

    def test_yaml_writer_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(dump_result="injected: true\n")
        path = tmp_path / "output.yaml"

        writer = YAMLWriter(adapter=adapter)
        writer.write({"hello": "world"}, str(path))

        assert path.read_text(encoding="utf-8") == "injected: true\n"
        assert adapter.last_data == {"hello": "world"}

    def test_env_writer_uses_injected_adapter(self, tmp_path):
        adapter = RecordingAdapter(dump_result="INJECTED=true\n")
        path = tmp_path / "output.env"

        writer = EnvWriter(adapter=adapter)
        writer.write({"hello": "world"}, str(path))

        assert path.read_text(encoding="utf-8") == "INJECTED=true\n"
        assert adapter.last_data == {"hello": "world"}
