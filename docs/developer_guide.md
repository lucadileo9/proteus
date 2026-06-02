# Developer Guide

This guide is intended for developers who want to contribute to Proteus or understand the underlying development workflow and automation.

---

## Educational Purpose

This project was developed as part of a Software Engineering course to demonstrate:

- **Design Patterns in Practice**: Real-world application of GoF patterns.
- **SOLID Principles**: Clean architecture with clear responsibilities.
- **Extensibility**: Open/Closed principle in action.
- **Modular Design**: Separation of concerns and loose coupling.

The codebase is intentionally structured to be readable and educational, with explicit pattern documentation in docstrings and clear separation between responsibilities. However, Proteus is designed for real-world use, solving actual problems in configuration management.

---

## 🛠️ Development Workflow

Proteus uses a `Makefile` to standardize common development tasks across different operating systems.

### Initial Setup
1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   ```
2. **Install development dependencies**:
   ```bash
   make install-dev
   ```
   *This command also installs the pre-commit hooks.*

### The Golden Rule: `make all`
Before committing any code, you should always run:
```bash
make all
```
This command executes the following sequence:
1. **`format`**: Ruff formats the code and applies safe auto-fixes.
2. **`lint`**: Ruff checks for style violations and logical errors.
3. **`typecheck`**: Mypy verifies static type hints in `src/`.
4. **`test`**: Pytest runs the full suite and verifies coverage (>95%).

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

## 🔍 Toolchain Details

### Ruff (Linter & Formatter)
We use [Ruff](https://github.com/astral-sh/ruff) because it is significantly faster than Black and Flake8 combined. It is configured in `pyproject.toml` with a strict set of rules (Bugbear, Isort, Simplify, etc.).
- **Exceptions**: Print statements are allowed in `examples/` and `tests/`.

### Mypy (Static Typing)
Proteus enforces strict typing in the `src/` directory. All public APIs must have type hints.
- **Pragmatic Testing**: To keep tests readable, Mypy is configured to be more lenient in the `tests/` directory (see [tests.md](tests.md)).

### Bandit (Security)
Bandit scans the codebase for common security issues. It is integrated into the CI pipeline to ensure that no obvious vulnerabilities are introduced.

### Tox (Cross-version Testing)
While you develop on your local Python version, [Tox](https://tox.wiki/) allows you to test Proteus against multiple Python versions (3.8 through 3.12) simultaneously in isolated environments.
```bash
make tox
```

---

## 🤖 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) uses an **Hybrid Strategy**:

| Trigger | Strategy | Machines |
|---------|----------|----------|
| **Every Push** | Fast Test (Latest Python only) | 3 (Win, Linux, Mac) |
| **Pull Request** | Full Matrix (All versions) | 15 (5 versions × 3 OS) |

---

## 🤝 How to Contribute

1. **Check the issues**: Look for open issues labeled `good first issue` or `help wanted`.
2. **Write Tests First**: Every bug fix or new feature must include corresponding tests in the `tests/unit/` or `tests/integration/` directories.
3. **Keep Docs Updated**: If you change an API or add a format, update the relevant file in `docs/`.
4. **Pass the Suite**: Ensure `make all` passes 100% on your machine.
5. **Open a PR**: Target the `develop` branch for new features.

---

## Acknowledgments

- **Gang of Four** - For the foundational design patterns.
- **Python Community** - For excellent libraries and best practices.
- **Software Engineering Course** - For inspiring this project.
