# Readers

> **GoF Pattern: Template Method** — Defines a fixed reading algorithm; subclasses supply only the format-specific parsing step.

## Overview

Every reader follows the same four-step algorithm defined by
`BaseReader.parse()`. Concrete readers override a single abstract method
(`_parse_content`) that delegates to the matching Adapter.

## BaseReader

Defined in `src/proteus/readers/base.py`.

### Template Method — `parse(filepath: str | Path) → Dict[str, Any]`

| Step | Method | Override? | Description |
|------|--------|-----------|-------------|
| 1 | `_validate(filepath)` | Hook | Checks that the file exists and is a regular file. |
| 2 | `_read_file(filepath)` | Hook | Reads the file content as UTF-8 text. |
| 3 | `_parse_content(raw)` | **Abstract** | Converts raw text into a `Dict[str, Any]` (IR). |
| 4 | `_normalize_data(data)` | Hook | Optional post-processing (identity by default). |

**Hook** means the method has a default implementation but can be overridden.
**Abstract** means the method *must* be implemented by every subclass.

## Concrete Readers

| Class | Module | Adapter Used |
|-------|--------|-------------|
| `JSONReader` | `readers/json_reader.py` | `JSONAdapter` |
| `YAMLReader` | `readers/yaml_reader.py` | `YAMLAdapter` |
| `EnvReader`  | `readers/env_reader.py`  | `EnvAdapter`  |

Each concrete reader:

1. Accepts an optional adapter in `__init__`.
2. Falls back to the built-in adapter when none is injected.
3. Implements `_parse_content(raw)` by calling `self._adapter.load(raw)`.

No other method needs overriding.

## Errors

| Exception | Raised When |
|-----------|-------------|
| `FileNotFoundError` | File does not exist. |
| `ValueError` | Path is not a regular file, or content cannot be parsed. |

## Usage

```python
from proteus.readers.json_reader import JSONReader

reader = JSONReader()
data = reader.parse("config.json")
print(data)  # {'database': {'host': 'localhost', ...}}
```

If you need custom parsing behavior, inject a custom adapter:

```python
from proteus.readers.json_reader import JSONReader
from my_adapters import MyJSONAdapter

reader = JSONReader(adapter=MyJSONAdapter())
```

> **Note:** In most cases you should use `ConfigurationManager.load()` instead
> of readers directly — the manager selects the correct reader automatically.

### Path Support

`parse()` accepts either a string path or a `pathlib.Path` object.
