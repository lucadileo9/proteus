# Proteus

**Unified Configuration Management Library for Python**

[![CI](https://github.com/lucadileo9/proteus/actions/workflows/ci.yml/badge.svg)](https://github.com/lucadileo9/proteus/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/lucadileo9/proteus/branch/main/graph/badge.svg)](https://codecov.io/gh/lucadileo9/proteus)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/github/license/lucadileo9/proteus)

Proteus is a Python library that provides a clean, pattern-based approach to managing application configurations. It allows you to load settings from multiple formats (JSON, YAML, TOML, ENV) and access them through a unified interface, regardless of the source format.

---

## Features

- **Multi-format Support**: Load configurations from JSON, YAML, and TOML files seamlessly.
- **Unified Interface**: Access all settings through a single, consistent API with dot-notation.
- **Namespacing Support**: Inject configurations into specific nested paths to avoid collisions.
- **Smart Merging**: Combine multiple configuration files with intelligent deep-merge.
- **Translation Engine**: Convert configuration files between formats programmatically.
- **Thread-Safe**: Optional singleton access via `ConfigurationManager.instance()`.
- **Context Manager**: Use `with ConfigurationManager.temporary()` for isolated workspaces.
- **Easily Extensible**: Add support for new formats with minimal code.
- **Zero Heavy Dependencies**: Only requires `pyyaml` and `python-dotenv`.

---

## 🛠️ CLI

Proteus comes with a built-in Command Line Interface for quick configuration tasks:

```bash
# Convert between formats
proteus translate settings.env settings.json

# Read a specific key
proteus get config.yaml database.host

# Merge multiple files into one
proteus merge base.json prod.env --out final.toml
```

See [CLI Documentation](https://github.com/lucadileo9/proteus/blob/main/docs/cli.md) for more details.

---

## Quick Start

### Installation

Install Proteus directly from PyPI:

```bash
pip install proteus-config
```

### Basic Usage

```python
from proteus import Proteus
# or from proteus import ConfigurationManager

config = Proteus()
config.load("examples/configs/app.yaml")

print(config.get("app_name"))
print(config.get("database.host"))
print(config.get("server.port"))
```

For a shared application-wide instance, use `Proteus.instance()`.

### Loading OS Environment Variables

For containerized or production environments (like Docker or Kubernetes) where configurations are passed as system environment variables, you can load them directly using `load_environ`:

```python
from proteus import Proteus

config = Proteus()

# Load OS environment variables starting with specified prefixes
config.load_environ(prefixes=["DATABASE_", "APP_"])

# Environment variables like DATABASE__HOST=localhost are automatically nested
print(config.get("DATABASE.HOST"))  # Prints 'localhost'
```

For detailed and comprehensive examples covering all formats, see the [examples/](https://github.com/lucadileo9/proteus/tree/main/examples) directory.

---

## Architecture and Design Patterns

Proteus is built on a foundation of proven design patterns from the Gang of Four catalog:

- **Optional Singleton Pattern**: Global point of access to configuration.
- **Context Manager**: Isolated temporary workspaces.
- **Facade Pattern**: Simplified API over complex orchestration.
- **Factory Method Pattern**: Transparent format detection and creator selection.
- **Template Method Pattern**: Rigid algorithms for I/O with format-specific hooks.
- **Adapter Pattern**: Decoupling from third-party parsing libraries.

For detailed architecture documentation and diagrams, see:
- [Architecture](https://github.com/lucadileo9/proteus/blob/main/docs/architecture.md)
- [ConfigurationManager](https://github.com/lucadileo9/proteus/blob/main/docs/manager.md)
- [Format Creators](https://github.com/lucadileo9/proteus/blob/main/docs/formats.md)
- [Readers](https://github.com/lucadileo9/proteus/blob/main/docs/readers.md)
- [Writers](https://github.com/lucadileo9/proteus/blob/main/docs/writers.md)
- [Test Suite](https://github.com/lucadileo9/proteus/blob/main/docs/tests.md)

---

## Development and Contributing

If you wish to contribute to the project or understand the development workflow, please refer to our **[Developer Guide](https://github.com/lucadileo9/proteus/blob/main/docs/developer_guide.md)**.

### Project Structure

```
proteus/
├── src/proteus/           # Source code
│   ├── core.py            # ConfigurationManager
│   ├── exceptions.py      # Custom exceptions
│   ├── adapters/          # Format adapters
│   ├── formats/           # Creator classes for readers/writers
│   ├── readers/           # Template Method readers
│   └── writers/           # Template Method writers
├── examples/             # Usage examples and configs
└── docs/                 # Documentation
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/lucadileo9/proteus/blob/main/LICENSE) file for details.

---

## Contact

**Luca Di Leo**
- GitHub: [@lucadileo9](https://github.com/lucadileo9)
- Repository: [proteus](https://github.com/lucadileo9/proteus)

---
