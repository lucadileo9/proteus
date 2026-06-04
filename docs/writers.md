# Writers

> **GoF Pattern: Template Method** — Defines a fixed writing algorithm; subclasses supply only the format-specific serialization step.

## Overview

Mirrors the Reader layer. Every writer follows a three-step algorithm
defined by `BaseWriter.write()`. Concrete writers override a single
abstract method (`_serialize`) that delegates to the matching Adapter.

## BaseWriter

Defined in `src/proteus/writers/base.py`.

### Template Method — `write(data: Dict[str, Any], filepath: str | Path) → None`

| Step | Method | Override? | Description |
|------|--------|-----------|-------------|
| 1 | `_validate(data, filepath)` | Hook | Checks that `data` is a dict and the parent directory exists. |
| 2 | `_serialize(data)` | **Abstract** | Converts the IR dict into a format-specific string. |
| 3 | `_write_file(content, filepath)` | Hook | Writes the string to disk as UTF-8. |

**`GenericWriter`**: Implements the variable `_serialize` step by delegating directly to `self._adapter.dump()`. Most formats use this "bridge".
**Concrete Writers**: (e.g. `JSONWriter`, `YAMLWriter`) inherit from `GenericWriter`. They serve as **semantic shells** that specify a default adapter.


## Concrete Writers

| Class | Module | Adapter Used |
|-------|--------|-------------|
| `JSONWriter` | `writers/json_writer.py` | `JSONAdapter` |
| `YAMLWriter` | `writers/yaml_writer.py` | `YAMLAdapter` |
| `TOMLWriter` | `writers/toml_writer.py` | `TOMLAdapter` |
| `EnvWriter`  | `writers/env_writer.py`  | `EnvAdapter`  |

Each concrete writer:

1. Accepts an optional adapter in `__init__`.
2. Falls back to the built-in adapter when none is injected.
3. Implements `_serialize(data)` by calling `self._adapter.dump(data)`.

## Errors

| Exception | Raised When |
|-----------|-------------|
| `TypeError` | `data` is not a dict. |
| `FileNotFoundError` | Parent directory does not exist. |
| `ValueError` | Data cannot be serialized. |

## Usage

```python
from proteus.writers.json_writer import JSONWriter

writer = JSONWriter()
writer.write({"debug": True, "port": 8080}, "output.json")
```

If you need custom serialization behavior, inject a custom adapter:

```python
from proteus.writers.json_writer import JSONWriter
from my_adapters import MyJSONAdapter

writer = JSONWriter(adapter=MyJSONAdapter())
```

> **Note:** Prefer `ConfigurationManager.translate()` for format conversion —
> it handles reader + writer coordination automatically.

### Path Support

`write()` accepts either a string path or a `pathlib.Path` object.
