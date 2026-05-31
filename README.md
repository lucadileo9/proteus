# Proteus

**Unified Configuration Management Library for Python**

[![CI](https://github.com/lucadileo9/proteus/actions/workflows/ci.yml/badge.svg)](https://github.com/lucadileo9/proteus/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/lucadileo9/proteus/branch/main/graph/badge.svg)](https://codecov.io/gh/lucadileo9/proteus)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

Proteus is a Python library that provides a clean, pattern-based approach to managing application configurations. It allows you to load settings from multiple formats (JSON, YAML, ENV) and access them through a unified interface, regardless of the source format.


---

## ✨ Features

- **Multi-format Support**: Load configurations from JSON and YAML files seamlessly
- **Unified Interface**: Access all settings through a single, consistent API with dot-notation
- **Smart Merging**: Combine multiple configuration files with intelligent deep-merge
- **Translation Engine**: Convert configuration files between formats (e.g., YAML to JSON) programmatically
- **Thread-Safe**: Optional singleton access via `ConfigurationManager.instance()`
- **Context Manager**: Use `with ConfigurationManager.temporary()` for isolated workspaces
- **Easily Extensible**: Add support for new formats (TOML, XML, etc.) with minimal code
- **Zero Heavy Dependencies**: Only requires `pyyaml` for YAML support and `python-dotenv` for ENV

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/lucadileo9/proteus.git
cd proteus

# Install in development mode
pip install -e .
```

### Basic Usage

```python
from proteus import ConfigurationManager

config = ConfigurationManager()
config.load("config_examples/app.yaml")

print(config.get("app_name"))
print(config.get("database.host"))
print(config.get("server.port"))
```

Example output:

```text
proteus-demo
localhost
8080
```

For a shared application-wide instance, use `ConfigurationManager.instance()`.


---

## 🏗️ Architecture & Design Patterns

Proteus is built on a foundation of proven design patterns from the Gang of Four catalog:

### **Optional Singleton Pattern**
`ConfigurationManager.instance()` provides a single, global point of access to configuration when you want shared state, while direct construction still gives isolated instances.

### **Context Manager**
`ConfigurationManager.temporary()` creates a short-lived manager for `with` blocks, automatically resetting state when the block ends.

### **Facade Pattern**
Simple methods like `load()`, `get()`, `merge()`, `translate()`, and `translate_and_load()` hide the complexity of reader creation, file validation, and data normalization.

### **Factory Method Pattern**
`FormatCreator` automatically selects and instantiates the appropriate reader/writer pair based on file extension, making format detection transparent.

### **Template Method Pattern**
`BaseReader` and `BaseWriter` define fixed algorithms (validate → read → parse and validate → serialize → write) while allowing subclasses to customize only the format-specific steps.

### **Adapter Pattern**
Each adapter converts a specific format into a unified internal representation (IR), so the manager works with consistent data structures.

For detailed architecture documentation and diagrams, see:
- [docs/architecture.md](docs/architecture.md) - Comprehensive architecture explanation
- [docs/manager.md](docs/manager.md) - Manager behavior and API details
- [docs/formats.md](docs/formats.md) - Reader/writer factory details
- [docs/readers.md](docs/readers.md) - Template Method reader behavior
- [docs/writers.md](docs/writers.md) - Template Method writer behavior

---


## 🧪 Development

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
├── examples/             # Usage examples
├── config_examples/      # Sample configuration files
└── docs/                 # Documentation
```

### Toolchain

- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff) (ultra-fast all-in-one linter/formatter)
- **Type Checking**: [Mypy](http://mypy-lang.org/)
- **Testing**: [Pytest](https://pytest.org/) with [Pytest-Cov](https://github.com/pytest-dev/pytest-cov)
- **Security**: [Bandit](https://github.com/PyCQA/bandit)
- **Automation**: [Tox](https://tox.wiki/) (multi-version testing) and [Make](https://www.gnu.org/software/make/)

### Makefile Commands (Cross-platform)

| Command | Description |
|---------|-------------|
| `make install-dev` | Install all development dependencies and pre-commit hooks |
| `make test` | Run the test suite and generate coverage report |
| `make lint` | Run Ruff to check for code style and logical errors |
| `make format` | Automatically format code and fix linting issues |
| `make typecheck` | Run Mypy to verify static type hints |
| `make tox` | Run tests against all supported Python versions |
| `make all` | Run format, lint, typecheck, and tests in sequence |
| `make build` | Prepare the package for distribution (wheel/sdist) |

---

## 🎓 Educational Purpose

This project was developed as part of a Software Engineering course to demonstrate:

- **Design Patterns in Practice**: Real-world application of GoF patterns
- **SOLID Principles**: Clean architecture with clear responsibilities
- **Extensibility**: Open/Closed principle in action
- **Modular Design**: Separation of concerns and loose coupling

The codebase is intentionally structured to be readable and educational, with:
- Explicit pattern documentation in docstrings
- Clear separation between pattern responsibilities
- Comprehensive architecture documentation

However, **Proteus is designed for real use**. The patterns aren't just academic exercises—they solve actual problems in configuration management and provide a foundation for production-ready features.


---

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Gang of Four** - For the foundational design patterns
- **Python Community** - For excellent libraries and best practices
- **Software Engineering Course** - For inspiring this project

---

## 📞 Contact

**Luca Di Leo**
- GitHub: [@lucadileo9](https://github.com/lucadileo9)
- Repository: [proteus](https://github.com/lucadileo9/proteus)

---

**Built with ❤️ and design patterns**
