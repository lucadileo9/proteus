# Proteus

**Unified Configuration Management Library for Python**



Proteus is a Python library that provides a clean, pattern-based approach to managing application configurations. It allows you to load settings from multiple formats (JSON, YAML, ENV) and access them through a unified interface, regardless of the source format.


---

## ✨ Features

- **Multi-format Support**: Load configurations from JSON and YAML files seamlessly
- **Unified Interface**: Access all settings through a single, consistent API with dot-notation
- **Smart Merging**: Combine multiple configuration files with intelligent deep-merge
- **Thread-Safe**: Optional singleton access via `ConfigurationManager.instance()`
- **Context Manager**: Use `with ConfigurationManager.temporary()` for isolated workspaces
- **Easily Extensible**: Add support for new formats (TOML, XML, etc.) with minimal code
- **Zero External Dependencies**: Only requires `pyyaml` for YAML support

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
Simple methods like `load()`, `get()`, `translate()`, and `translate_and_load()` hide the complexity of reader creation, file validation, and data normalization.

### **Factory Method Pattern**
`FormatCreator` automatically selects and instantiates the appropriate reader/writer pair based on file extension, making format detection transparent.

### **Template Method Pattern**
`BaseReader` and `BaseWriter` define fixed algorithms (validate → read → parse and validate → serialize → write) while allowing subclasses to customize only the format-specific steps.

### **Adapter Pattern**
Each adapter converts a specific format into a unified internal representation, so the manager works with consistent data structures.

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

### Requirements

- **Python**: 3.8 or higher
- **Runtime Dependencies**: `pyyaml>=6.0`
- **Development** (optional): `pytest`, `black`, `ruff`, `mypy`

### Practical Examples

```python
from pathlib import Path
from proteus import ConfigurationManager

config = ConfigurationManager.temporary()
config.load(Path("config_examples/app.yaml"))
config.translate_and_load(Path("config_examples/app.yaml"), Path("config_examples/output/app.json"))
print(config.get("database.host"))
```

```python
from proteus import ConfigurationManager

with ConfigurationManager.temporary() as config:
	config.load("config_examples/app.yaml")
	print(config.get("server.port"))
```


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

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to public APIs
- Update documentation for new features
- Ensure backward compatibility

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


---

**Built with ❤️ and design patterns**
