# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-01
### Added
- Full TOML format support (read, write, translate).
- Security scanning with Bandit integrated into the CI/CD pipeline.
- Multi-version Python testing with Tox (supporting Python 3.8 to 3.12).
- Secure PyPI publication workflow using GitHub Trusted Publishing.
- Add GitHub Issue Templates for Bug Reports and Feature Requests.
- Interactive translation demo script (`examples/03_translate.py`).
- Comprehensive Developer Guide.

### Changed
- Consolidated all linting and formatting under Ruff for extreme performance.
- Reorganized `tests/` into a modular `unit/` and `integration/` structure.
- Refactored `examples/` into a numbered, cohesive guided tour.
- Modernized `Makefile` to be fully cross-platform (Windows, Linux, macOS).
- Enhanced `README.md` with professional status badges and exhaustive feature lists.

### Fixed
- Enforced strict Mypy type-checking on `src/` while maintaining pragmatic test typing.
- Corrected several line-length violations and documentation typos.
- Explicitly included `py.typed` and `LICENSE` in the package distribution.

## [0.1.0] - 2026-05-30
### Added
- Initial release
- JSON, YAML, ENV format support
- ConfigurationManager with optional Singleton access + Facade
- Deep merge for multiple config files
- Format translation (`translate()` and `translate_and_load()`)
- Support for `pathlib.Path` in public APIs
- Initial test suite with high coverage
