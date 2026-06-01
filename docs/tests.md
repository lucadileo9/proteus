# Test Suite

The Proteus test suite is designed for high reliability and behavior-focused verification, achieving >95% coverage across all components.

## Structure

The tests are organized into **unit** and **integration** categories, mirroring the source code structure.

```text
tests/
├── unit/
│   ├── adapters/        # Isolated tests for JSON, YAML, TOML, ENV adapters
│   ├── readers/         # Template Method tests for each Reader
│   └── writers/         # Template Method tests for each Writer
├── integration/
│   ├── test_manager.py  # Facade & Singleton orchestration tests
│   ├── test_formats.py  # Factory Method (FormatCreator) integration
│   └── test_dependency_injection.py
├── conftest.py          # Shared fixtures (temporary files, fresh managers)
└── sample_data.py       # Centralized test inputs (valid/invalid strings and dicts)
```

`sample_data.py` centralises all test inputs so no test file hard-codes raw strings. This makes it easy to change a sample and have every dependent test pick up the new value automatically.

---

## Testing Philosophy

### Pragmatic Typing
While the core library is strictly typed, the test suite uses **pragmatic typing**. We intentionally omit return type annotations (`-> None`) and complex parameter hints in most test functions to maximize readability and reduce maintenance overhead. Mypy is configured to allow untyped definitions specifically for the `tests/` directory.

### What Is Not Tested (by Design)
Private parsing logic inside adapters is not tested directly through readers: readers and writers delegate to adapters, and adapters are tested independently in `unit/adapters/`. The Template Method steps (`_validate`, `_read_raw`, `_parse_content`) are exercised as side effects of calling the public `parse()` / `write()` methods.

---

## Noteworthy Testing Decisions

### Abstract Class Enforcement
All abstract classes — `BaseAdapter`, `FormatCreator`, `BaseReader`, `BaseWriter` — are verified to ensure they cannot be instantiated directly and that subclasses must implement all required abstract methods.

### Round-Trip Tests
Every reader/writer pair and every adapter has at least one round-trip test (`write → read` or `dump → load`). This is the strongest guarantee that Proteus can safely serialize and deserialize data without loss of integrity.

### Uniform Error Surface
The Template Method ensures that all formats raise consistent exceptions for common failures:
- **Readers**: `FileNotFoundError` for missing files, `ValueError` for directories.
- **Writers**: `TypeError` for non-dict data, `FileNotFoundError` for missing output directories.

---

## Toolchain & Automation

Proteus uses a modern automation stack to ensure quality:

| Tool | Purpose | Command |
|------|---------|---------|
| **Pytest** | Test runner and fixture management | `make test` |
| **Ruff** | Linting and Formatting (Standard PEP 8) | `make lint` / `make format` |
| **Mypy** | Static type checking (Strict on `src/`) | `make typecheck` |
| **Bandit** | Security vulnerability scanning | `make lint` (integrated) |
| **Tox** | Multi-version Python compatibility testing | `make tox` |

Run `make all` before every commit to ensure the entire suite passes.

---
