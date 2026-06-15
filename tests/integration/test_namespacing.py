import json

import pytest

from proteus.core import ConfigurationManager


def test_load_with_namespace(tmp_path):
    """load() with a namespace injects the config under a nested key."""
    path = tmp_path / "groups.json"
    path.write_text(json.dumps({"IT": 123, "HR": 456}), encoding="utf-8")

    mgr = ConfigurationManager()
    mgr.load(str(path), namespace="telegram.groups")

    assert mgr.get("telegram.groups.IT") == 123
    assert mgr.get("telegram.groups.HR") == 456
    # Verify the structure is correct
    assert mgr.get("telegram.groups") == {"IT": 123, "HR": 456}


def test_load_with_deep_namespace(tmp_path):
    """load() works with multi-level namespaces."""
    path = tmp_path / "data.json"
    path.write_text(json.dumps({"key": "value"}), encoding="utf-8")

    mgr = ConfigurationManager()
    mgr.load(str(path), namespace="a.b.c.d")

    assert mgr.get("a.b.c.d.key") == "value"


def test_merge_with_namespace(tmp_path):
    """merge() also supports the namespace parameter."""
    path = tmp_path / "extra.json"
    path.write_text(json.dumps({"new": "val"}), encoding="utf-8")

    mgr = ConfigurationManager()
    mgr.set("existing", True)
    mgr.merge(str(path), namespace="nested")

    assert mgr.get("existing") is True
    assert mgr.get("nested.new") == "val"


def test_invalid_namespace_raises_error(tmp_path):
    """Invalid namespaces should raise InvalidKeyError."""
    path = tmp_path / "cfg.json"
    path.write_text("{}", encoding="utf-8")

    mgr = ConfigurationManager()
    from proteus.exceptions import InvalidKeyError

    with pytest.raises(InvalidKeyError):
        mgr.load(str(path), namespace=".invalid")


def test_translate_and_load_with_namespace(tmp_path):
    """translate_and_load() correctly translates and then injects into a namespace."""
    json_path = tmp_path / "data.json"
    json_path.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    yaml_path = tmp_path / "data.yaml"

    mgr = ConfigurationManager()
    mgr.translate_and_load(str(json_path), str(yaml_path), namespace="translated")

    assert yaml_path.exists()
    assert mgr.get("translated.key") == "value"
