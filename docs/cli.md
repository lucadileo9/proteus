# CLI — Command Line Interface

Proteus provides a powerful Command Line Interface (CLI) to interact with configuration files directly from your terminal.

## Installation

The CLI is automatically installed with the package. You can verify it by running:

```bash
proteus --version
```

## Global Options

- `--version`: Show the version number and exit.
- `--help`: Show help for a specific command.

---

## Commands

### `get`

Read a specific value from a configuration file.

**Usage:**
```bash
proteus get <file> <key> [--cast <type>]
```

**Examples:**
```bash
# Read a nested key from JSON
proteus get config.json database.host

# Read from .env and cast to integer
proteus get .env PORT --cast int
```

**Supported Casts:** `int`, `float`, `bool`, `str`.

---

### `set`

Modify a value in a configuration file and save the result.

**Usage:**
```bash
proteus set <file> <key> <value> [--out <dest>]
```

**Examples:**
```bash
# Update a value in place (overwrites config.yaml)
proteus set config.yaml app.debug true

# Update and save to a new file
proteus set config.yaml version "2.0.0" --out config_v2.yaml
```

---

### `merge`

Merge multiple configuration files into a single output file. Later files override earlier ones.

**Usage:**
```bash
proteus merge <files...> --out <dest>
```

**Example:**
```bash
# Merge JSON, YAML and ENV into a final TOML file
proteus merge base.json override.yaml prod.env --out final.toml
```

---

### `translate`

Convert a configuration file from one format to another.

**Usage:**
```bash
proteus translate <input> <output>
```

**Example:**
```bash
# Convert ENV to JSON
proteus translate settings.env settings.json
```

---

### `view`

Display the merged configuration of one or more files as JSON.

**Usage:**
```bash
proteus view [files...]
```

**Example:**
```bash
# See the result of merging two files
proteus view base.yaml prod.env
```

---

### `list-files`

List the absolute paths of configuration files that Proteus loads.

**Usage:**
```bash
proteus list-files [files...]
```

**Example:**
```bash
proteus list-files settings.yaml
# → /home/user/project/settings.yaml
```

---

## Exit Codes

The CLI follows standard Unix conventions for exit codes:
- `0`: Success.
- `1`: Failure (e.g., file not found, invalid key, unsupported format).

## Scripting

The CLI is designed to be stateless and script-friendly. You can use it in your Bash or CI/CD pipelines:

```bash
#!/bin/bash
DB_PORT=$(proteus get config.yaml db.port --cast int)

if [ "$DB_PORT" -eq 5432 ]; then
  echo "Production database detected."
fi
```
