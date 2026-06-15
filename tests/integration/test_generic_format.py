from typing import Any, Dict

from proteus.adapters.base import BaseAdapter
from proteus.core import ConfigurationManager


class MockAdapter(BaseAdapter):
    def load(self, raw: str) -> Dict[str, Any]:
        return {"mock": raw.strip()}

    def dump(self, data: Dict[str, Any]) -> str:
        return f"MOCK|{data.get('mock', 'none')}"


class TestRegisterAdapter:
    """Test the high-level register_adapter shortcut."""

    def test_register_and_load(self, tmp_path):
        path = tmp_path / "test.mock"
        path.write_text("hello", encoding="utf-8")

        mgr = ConfigurationManager()
        mgr.register_adapter([".mock"], MockAdapter())

        mgr.load(str(path))
        assert mgr.get("mock") == "hello"

    def test_register_and_translate(self, tmp_path):
        src = tmp_path / "input.mock"
        src.write_text("world", encoding="utf-8")
        dst = tmp_path / "output.json"

        mgr = ConfigurationManager()
        mgr.register_adapter([".mock"], MockAdapter())

        mgr.translate(str(src), str(dst))

        import json

        result = json.loads(dst.read_text(encoding="utf-8"))
        assert result == {"mock": "world"}

    def test_register_and_translate_to_custom(self, tmp_path):
        """Translate from native format to custom format."""
        src = tmp_path / "input.json"
        src.write_text('{"mock": "world"}')
        dst = tmp_path / "output.mock"

        mgr = ConfigurationManager()
        mgr.register_adapter([".mock"], MockAdapter())

        mgr.translate(str(src), str(dst))

        assert dst.read_text(encoding="utf-8") == "MOCK|world"

    def test_register_multiple_extensions(self, tmp_path):
        p1 = tmp_path / "a.m1"
        p1.write_text("v1", encoding="utf-8")
        p2 = tmp_path / "b.m2"
        p2.write_text("v2", encoding="utf-8")

        mgr = ConfigurationManager()
        mgr.register_adapter([".m1", ".m2"], MockAdapter())

        mgr.load(str(p1))
        mgr.merge(str(p2))

        assert mgr.get("mock") == "v2"  # Overwritten by merge

    def test_generic_reader_direct(self):
        """GenericReader correctly delegates to the injected adapter."""
        from proteus.readers.generic import GenericReader

        adapter = MockAdapter()
        reader = GenericReader(adapter=adapter)
        assert reader._parse_content("hello") == {"mock": "hello"}

    def test_generic_writer_direct(self):
        """GenericWriter correctly delegates to the injected adapter."""
        from proteus.writers.generic import GenericWriter

        adapter = MockAdapter()
        writer = GenericWriter(adapter=adapter)
        assert writer._serialize({"mock": "world"}) == "MOCK|world"
