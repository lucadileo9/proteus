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
| `GenericFormatCreator` | (User-defined) | `GenericReader` | `GenericWriter` |

## The Generic Format System

To make Proteus easily extensible, we provide a **Generic Delegation** layer.

`GenericFormatCreator` acts as a universal bridge: it takes any `BaseAdapter` and uses it to drive standard `GenericReader` and `GenericWriter` instances. This is what powers the `register_adapter()` shortcut.

When translating between formats, two *different* creators collaborate:

```
translate("app.yaml", "app.json")
    ├── YAMLFormatCreator.create_reader()  →  reads YAML
    └── JSONFormatCreator.create_writer()  →  writes JSON
```

## Adding a New Format

Proteus is designed to be easily extensible (Open/Closed Principle). You can add support for a new format in two ways:

### 1. The Shortcut (Recommended)
If you only need standard parsing and serialization, just implement a subclass of `BaseAdapter` and use `register_adapter()`. Proteus will automatically handle the Reader, Writer, and Factory layers for you.

```python
from proteus import ConfigurationManager, BaseAdapter

class MyFormatAdapter(BaseAdapter):
    def load(self, raw): ...
    def dump(self, data): ...

config = ConfigurationManager()
# Automatically creates a GenericFormatCreator for you
config.register_adapter(extensions=[".myf"], adapter=MyFormatAdapter())
```

### 2. The Full Pattern Stack
If you need highly custom behavior (e.g. specialized file validation or post-processing), you can implement the full stack manually:

1. **Adapter** — Create `MyAdapter(BaseAdapter)`.
2. **Reader** — Create `MyReader(BaseReader)` using your adapter.
3. **Writer** — Create `MyWriter(BaseWriter)` using your adapter.
4. **Creator** — Create `MyFormatCreator(FormatCreator)` returning your custom reader/writer.

Register it at runtime:
```python
config.register_creator(MyFormatCreator())
```
