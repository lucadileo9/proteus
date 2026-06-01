"""
Shared sample data for Proteus tests.

Provides constant dictionaries and strings used across
reader and writer test modules.
"""


# ------------------------------------------------------------------ #
# Sample data                                                         #
# ------------------------------------------------------------------ #

SAMPLE_NESTED = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "proteus_db",
    },
    "app": {
        "name": "Proteus",
        "debug": True,
        "version": "1.0.0",
    },
}

SAMPLE_FLAT = {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "APP_NAME": "Proteus",
    "DEBUG": "true",
}


# ------------------------------------------------------------------ #
# JSON content                                                        #
# ------------------------------------------------------------------ #

SAMPLE_JSON = """{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "proteus_db"
  },
  "app": {
    "name": "Proteus",
    "debug": true,
    "version": "1.0.0"
  }
}"""

INVALID_JSON = "{not valid json"
JSON_ARRAY_ROOT = "[1, 2, 3]"


# ------------------------------------------------------------------ #
# YAML content                                                        #
# ------------------------------------------------------------------ #

SAMPLE_YAML = """database:
  host: localhost
  port: 5432
  name: proteus_db
app:
  name: Proteus
  debug: true
  version: '1.0.0'
"""

INVALID_YAML = ":\n  :\n    - ][invalid"
YAML_EMPTY = ""
YAML_ONLY_COMMENTS = "# this is a comment\n# another comment\n"
YAML_SCALAR_ROOT = "just a string"


# ------------------------------------------------------------------ #
# ENV content                                                         #
# ------------------------------------------------------------------ #

SAMPLE_ENV = """DB_HOST=localhost
DB_PORT=5432
APP_NAME=Proteus
DEBUG=true
"""

ENV_WITH_QUOTES = """GREETING="hello world"
PATH_VAR='/usr/local/bin'
"""

ENV_WITH_COMMENTS = """# database settings
DB_HOST=localhost
# app settings
APP_NAME=Proteus
"""

ENV_EMPTY_VALUE = "EMPTY_KEY=\n"

ENV_EMPTY = ""


# ------------------------------------------------------------------ #
# TOML content                                                        #
# ------------------------------------------------------------------ #

SAMPLE_TOML = """[database]
host = "localhost"
port = 5432
name = "proteus_db"

[app]
name = "Proteus"
debug = true
version = "1.0.0"
"""

INVALID_TOML = '[database\nhost = "localhost"'
TOML_SCALAR_ROOT = '"just a string"'
