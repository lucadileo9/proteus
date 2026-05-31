# Proteus - Project Instructions

Proteus is a unified configuration management library for Python. It provides a clean, pattern-based approach to managing application configurations across multiple formats (JSON, YAML, ENV) through a consistent API.

## Project Overview

- **Purpose**: Unified configuration management and translation.
- **Technologies**: Python 3.8+, `pyyaml`, `python-dotenv`.
- **Architecture**: Heavily based on Gang of Four (GoF) design patterns:
    - **Facade (`ConfigurationManager`)**: Simplifies interaction with the complex pattern stack.
    - **Optional Singleton**: Thread-safe global instance via `ConfigurationManager.instance()`.
    - **Factory Method (`FormatCreator`)**: Dynamically selects readers and writers based on file extensions.
    - **Template Method (`BaseReader`, `BaseWriter`)**: Defines a rigid skeleton for parsing and writing processes.
    - **Adapter (`BaseAdapter`)**: Wraps third-party libraries (`json`, `PyYAML`, `python-dotenv`) to provide a uniform internal representation (IR).

## Core Concepts

- **Intermediate Representation (IR)**: All configurations are normalized into a standard Python `Dict[str, Any]` in memory.
- **Dot-Notation Access**: Retrieve values using paths like `config.get("database.host")`.
- **Deep-Merge**: Multiple configuration sources can be loaded, with later sources intelligently overriding earlier ones.
- **Translation**: Supports converting between formats (e.g., YAML to JSON) without affecting internal state.

## Project Structure

```text
proteus/
├── src/proteus/           # Core library
│   ├── core.py            # ConfigurationManager (Facade/Singleton)
│   ├── exceptions.py      # Custom error hierarchy
│   ├── adapters/          # Format-specific library adapters
│   ├── formats/           # Creator factories for readers/writers
│   ├── readers/           # Template Method reader implementations
│   └── writers/           # Template Method writer implementations
├── tests/                 # Comprehensive test suite
├── docs/                  # Detailed architectural and component documentation
├── examples/              # Usage examples for end users
└── config_examples/       # Sample configuration files
```

## Development Workflow

### Key Commands

- **Run Tests**: `make test` (Uses `pytest` with coverage reporting).
- **Linting**: `make lint` (Uses `ruff`).
- **Formatting**: `make format` (Uses `black` and `ruff`).
- **Type Checking**: `make typecheck` (Uses `mypy`).
- **Full CI check**: `make all` (Runs format, lint, typecheck, and test).
- **Cleanup**: `make clean` (Removes caches and build artifacts).

### Standards and Conventions

- **Style**: Strictly follow PEP 8. Formatting is enforced via `black` (88 char line length).
- **Typing**: Use static type hints for all public methods and maintain `mypy` compatibility.
- **Documentation**: All public API methods must have docstrings explaining their purpose, parameters, and design pattern roles.
- **Testing**:
    - Aim for high coverage (target > 95%).
    - Add unit tests for every new feature or bug fix in the `tests/` directory.
    - Use `pytest` fixtures for setup/teardown (see `tests/conftest.py`).
- **Extensibility**: When adding support for new formats, implement a new `FormatCreator`, `Reader`, `Writer`, and `Adapter` without modifying the core `ConfigurationManager` logic (Open/Closed Principle).

## Adding a New Format

1.  **Adapter**: Create a subclass of `BaseAdapter` in `src/proteus/adapters/`.
2.  **Reader/Writer**: Create subclasses of `BaseReader` and `BaseWriter` in their respective directories.
3.  **Creator**: Create a subclass of `FormatCreator` in `src/proteus/formats/`.
4.  **Registration**: Register the new creator with the manager via `config.register_creator()`.
