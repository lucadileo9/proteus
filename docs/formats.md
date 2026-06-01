# Format Creators

> **GoF Pattern:  Abstract Factory** — Each creator encapsulates the construction of a reader/writer pair for a specific format.

## Overview

`FormatCreator` is the abstract creator. Each concrete creator couples a
reader and a writer of the **same** format, guaranteeing coherence.
`ConfigurationManager` depends only on `FormatCreator` — never on concrete
reader/writer classes (Dependency Inversion Principle).

## FormatCreator (Abstract)

Defined in `src/proteus/formats/base_format.py`.

| Abstract Factory Method | Returns | Description |
|----------------|---------|-------------|
| `create_reader()` | `BaseReader` | Instantiates the format-specific reader. |
| `create_writer()` | `BaseWriter` | Instantiates the format-specific writer. |
| `get_extensions()` | `List[str]` | File extensions this creator handles. |

## Built-in Creators

| Creator | Extensions | Reader | Writer |
|---------|-----------|--------|--------|
| `JSONFormatCreator` | `.json` | `JSONReader` | `JSONWriter` |
| `YAMLFormatCreator` | `.yaml`, `.yml` | `YAMLReader` | `YAMLWriter` |
| `TOMLFormatCreator` | `.toml` | `TOMLReader` | `TOMLWriter` |
| `EnvFormatCreator`  | `.env` | `EnvReader` | `EnvWriter` |

## How `translate()` Uses Two Creators

When translating between formats, two *different* creators collaborate:

```
translate("app.yaml", "app.json")
    ├── YAMLFormatCreator.create_reader()  →  reads YAML
    └── JSONFormatCreator.create_writer()  →  writes JSON
```

## Adding a New Format

To add support for a new format (e.g. TOML):

1. **Adapter** — Create `TOMLAdapter(BaseAdapter)` wrapping the TOML library.
2. **Reader** — Create `TOMLReader(BaseReader)` using `TOMLAdapter`.
3. **Writer** — Create `TOMLWriter(BaseWriter)` using `TOMLAdapter`.
4. **Creator** — Create `TOMLFormatCreator(FormatCreator)` returning the new reader/writer and declaring `[".toml"]`.

Register it at runtime:

```python
from proteus import ConfigurationManager

config = ConfigurationManager()
config.register_creator(TOMLFormatCreator())
config.load("settings.toml")  # works
```

No existing code needs to change (Open/Closed Principle).
