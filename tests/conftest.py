"""
Shared fixtures for Proteus tests.

Provides temporary directories used across reader and writer
test modules.  Sample data constants live in ``sample_data.py``.
"""

import pytest
from sample_data import SAMPLE_ENV, SAMPLE_JSON, SAMPLE_YAML

# ------------------------------------------------------------------ #
# Fixtures                                                            #
# ------------------------------------------------------------------ #


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory (pytest built-in tmp_path)."""
    return tmp_path


@pytest.fixture
def json_file(tmp_path):
    """Write sample JSON to a temp file and return the path."""
    path = tmp_path / "config.json"
    path.write_text(SAMPLE_JSON, encoding="utf-8")
    return str(path)


@pytest.fixture
def yaml_file(tmp_path):
    """Write sample YAML to a temp file and return the path."""
    path = tmp_path / "config.yaml"
    path.write_text(SAMPLE_YAML, encoding="utf-8")
    return str(path)


@pytest.fixture
def env_file(tmp_path):
    """Write sample .env to a temp file and return the path."""
    path = tmp_path / ".env"
    path.write_text(SAMPLE_ENV, encoding="utf-8")
    return str(path)


@pytest.fixture
def json_output(tmp_path):
    """Return a Path for a JSON output file (not yet written).

    Returned as Path (not str) so tests can both pass it to write()
    via str() and read it back via .read_text() without extra wrapping.
    """
    return tmp_path / "output.json"


@pytest.fixture
def yaml_output(tmp_path):
    """Return a Path for a YAML output file (not yet written).

    Returned as Path (not str) so tests can both pass it to write()
    via str() and read it back via .read_text() without extra wrapping.
    """
    return tmp_path / "output.yaml"


@pytest.fixture
def env_output(tmp_path):
    """Return a Path for an ENV output file (not yet written).

    Returned as Path (not str) so tests can both pass it to write()
    via str() and read it back via .read_text() without extra wrapping.
    """
    return tmp_path / "output.env"
