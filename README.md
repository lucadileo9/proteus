# Proteus

**Unified Configuration Management Library for Python**



Proteus is a Python library that provides a clean, pattern-based approach to managing application configurations. It allows you to load settings from multiple formats (JSON, YAML) and access them through a unified interface, regardless of the source format.


---

## ✨ Features

- **Multi-format Support**: Load configurations from JSON and YAML files seamlessly
- **Unified Interface**: Access all settings through a single, consistent API with dot-notation
- **Smart Merging**: Combine multiple configuration files with intelligent deep-merge
- **Thread-Safe**: Singleton pattern ensures safe concurrent access
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

To do...


---

## 🏗️ Architecture & Design Patterns

Proteus is built on a foundation of proven design patterns from the Gang of Four catalog:

### **Singleton Pattern**
`ConfigurationManager` ensures a single, global point of access to configuration throughout your application, preventing inconsistencies.

### **Facade Pattern**
Simple methods like `load()` and `get()` hide the complexity of parser creation, file validation, and data normalization.

### **Factory Method Pattern**
`ConfigParserFactory` automatically selects and instantiates the appropriate parser based on file extension, making format detection transparent.

### **Template Method Pattern**
`BaseParser` defines a fixed algorithm (validate → read → parse → normalize) while allowing subclasses to customize specific steps.

### **Adapter Pattern**
Each parser adapts its specific format into a unified internal representation, so the manager works with consistent data structures.

For detailed architecture documentation and diagrams, see:
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Comprehensive architecture explanation
- [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) - Visual diagrams (Class, Sequence, Component, etc.)
- [ROADMAP.md](ROADMAP.md) - Implementation phases and development plan

---


## 🧪 Development

### Project Structure

```
proteus/
├── src/proteus/           # Source code
│   ├── core.py           # ConfigurationManager
│   ├── factory.py        # Parser factory
│   ├── exceptions.py     # Custom exceptions
│   └── parsers/          # Parser implementations
│       ├── base.py       # Abstract base parser
│       ├── json_parser.py
│       └── yaml_parser.py
├── examples/             # Usage examples
├── config_examples/      # Sample configuration files
└── docs/                 # Documentation
```

### Requirements

- **Python**: 3.8 or higher
- **Runtime Dependencies**: `pyyaml>=6.0`
- **Development** (optional): `pytest`, `black`, `ruff`, `mypy`


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
