# Adapters

> **GoF Pattern: Adapter** — Wraps external libraries behind a uniform interface.

## Overview

The Adapter layer decouples readers and writers from the concrete parsing
libraries (`json`, `PyYAML`, `python-dotenv`). Swapping a library
requires changes only inside the relevant adapter — no reader, writer, or
client code is affected.

### GoF Roles

| Role      | Class                                    |
|-----------|------------------------------------------|
| Target    | `BaseAdapter` (abstract)                 |
| Adapter   | `JSONAdapter`, `YAMLAdapter`, `EnvAdapter` |
| Adaptee   | `json`, `yaml`, `dotenv`                 |

## BaseAdapter

Defined in `src/proteus/adapters/base.py`.

Abstract base class with two methods:

| Method | Signature | Description |
|--------|-----------|-------------|
| `load` | `(raw: str) → Dict[str, Any]` | Parse a raw string into the internal representation (IR). |
| `dump` | `(data: Dict[str, Any]) → str` | Serialize the IR into a format-specific string. |

Both methods raise `ValueError` on failure.

## Concrete Adapters

### JSONAdapter

**Adaptee:** `json` (stdlib) — `json.loads` / `json.dumps`

- `load()`: delegates to `json.loads()`. Rejects non-object roots.
- `dump()`: delegates to `json.dumps(indent=2, ensure_ascii=False)`.

### YAMLAdapter

**Adaptee:** `yaml` (PyYAML) — `yaml.safe_load` / `yaml.dump`

- `load()`: delegates to `yaml.safe_load()`. Returns `{}` for empty/comments-only files. Rejects non-mapping roots.
- `dump()`: delegates to `yaml.dump(default_flow_style=False, allow_unicode=True, sort_keys=False)`.

### EnvAdapter

**Adaptee:** `dotenv` (python-dotenv) — `dotenv_values`

- `load()`: delegates to `dotenv_values(stream=...)`. Returns `Dict[str, str]` — all values are strings. Keys with no value map to `""`.
- `dump()`: flattens nested dicts with `__` separator, converts keys to `UPPER_CASE`, and auto-quotes values containing spaces or special characters.

**Flattening example:**

```python
{"database": {"host": "localhost", "port": 5432}}
# becomes
DATABASE__HOST=localhost
DATABASE__PORT=5432
```

## Error Handling

All adapters convert library-specific exceptions into `ValueError` with a
descriptive message, keeping the original exception attached via `from`.
