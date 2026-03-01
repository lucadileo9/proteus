# Test Suite


## Structure

```
tests/
├── conftest.py          # shared fixtures (tmp files per format)
├── sample_data.py       # constants: dicts, raw strings, invalid inputs
├── test_adapters.py     # Adapter layer
├── test_env_reader.py   # EnvReader (Template Method)
├── test_json_reader.py  # JSONReader (Template Method)
├── test_yaml_reader.py  # YAMLReader (Template Method)
├── test_env_writer.py   # EnvWriter (Template Method)
├── test_json_writer.py  # JSONWriter (Template Method)
├── test_yaml_writer.py  # YAMLWriter (Template Method)
```

`sample_data.py` centralises all test inputs — valid, invalid, and edge-case — so
no test file hard-codes raw strings. This makes it easy to change a sample and
have every dependent test pick up the new value automatically.

---

## What Is Not Tested (by Design)

Private parsing logic inside adapters is not tested directly: readers and writers
delegate to adapters, and adapters are tested independently. The Template Method
steps (`_validate`, `_read_raw`, `_parse_content`) are exercised as side effects
of calling the public `parse()` / `write()` methods rather than patched or called
in isolation. This keeps tests behaviour-focused rather than implementation-focused.

---

## Noteworthy Testing Decisions

### Abstract Class Enforcement

All abstract classes — `BaseAdapter`, `FormatCreator` — are verified with three
levels of check:

1. Direct instantiation raises `TypeError`.
2. The correct methods appear in `__abstractmethods__`.
3. A subclass that implements **only some** abstract methods is still abstract
   and still raises `TypeError`.

Point 3 is the useful one: it catches incomplete implementations that could
otherwise silently bypass Python's ABC mechanism.

### Round-Trip Tests

Every reader/writer pair has at least one round-trip test:

```python
writer.write(data, path)
result = reader.parse(path)
assert result == data
```

These tests sit alongside adapters too (`dump → load`). They are the
strongest correctness guarantee because they exercise the serialisation and
deserialisation paths together, catching issues that unit tests on each half
would miss (e.g. the writer emitting a type the reader cannot recover).

### Template Method — Uniform Error Surface

All concrete readers raise the same two errors from `_validate()`:

| Scenario | Exception |
|----------|-----------|
| Path does not exist | `FileNotFoundError("File not found")` |
| Path is a directory | `ValueError("Not a regular file")` |

All concrete writers raise:

| Scenario | Exception |
|----------|-----------|
| `data` is not a `dict` | `TypeError("data must be a dict")` |
| Parent directory missing | `FileNotFoundError("Directory not found")` |

Testing these through the public `parse()` / `write()` methods (not by injecting
mocks) verifies that the Template Method's `_validate()` hook is actually called
and that the error messages are stable across all concrete subclasses.

### ENV-Specific Behaviours

The ENV format has several non-obvious behaviours that are tested explicitly:

- **All values are strings.** The `.env` format has no type system; `5432`,
  `true`, and `""` are all `str`. Tests assert `isinstance(v, str)` for every
  value in the parsed dict.
- **Flattening with `__`.** Nested dicts are flattened with a double-underscore
  separator and keys are uppercased:
  ```
  {"database": {"host": "localhost"}} → DATABASE__HOST=localhost
  ```
  Tests verify both the separator and the case conversion, including deeply
  nested structures (`A__B__C=deep`).
- **Auto-quoting.** Values containing spaces or `#` are wrapped in double quotes
  automatically on write. Values without special characters are *not* quoted.
  Tests assert the presence or absence of quotes explicitly.
- **`None` values.** A `None` value in the dict is serialised as an empty string
  (`KEY=`), which round-trips back to `""` on load. This is tested as an
  intentional contract, not an accident.

### YAML-Specific Behaviours

- **Empty input → `{}`.** An empty file and a file with only comments both
  produce an empty dict rather than `None`. Without this guard the adapter would
  return `None` and crash the caller.
- **`sort_keys=False`.** Insertion order is preserved on dump. A dedicated test
  writes a dict with keys in `z, a, m` order and verifies they appear in that
  same order in the YAML output.

### Singleton: Thread Safety

`ConfigurationManager` is verified to be thread-safe by creating 20 threads that
all call the constructor concurrently and collecting the instances:

```python
threads = [threading.Thread(target=lambda: instances.append(ConfigurationManager())) for _ in range(20)]
```

All 20 must be the exact same object (`is`, not `==`).

### Singleton: `_destroy()` vs `reset()`

These two housekeeping methods have different contracts and are tested separately:

| Method | Effect |
|--------|--------|
| `_destroy()` | Removes the singleton instance — the next call creates a brand-new object. |
| `reset()` | Clears the loaded configuration but keeps the same instance alive. |

The distinction matters: code that holds a reference to the manager before
`reset()` will still work; code that holds a reference before `_destroy()` will
be holding a stale object.

### Deep Merge

`_deep_merge(base, override)` is tested with two properties:

1. **Correctness** — nested keys from `override` win, untouched keys from `base`
   are preserved.
2. **Non-mutation** — `base` is not modified in place. This is tested by
   asserting that `base` equals its original value after the call.

Both are necessary: correctness is obvious, but non-mutation is easy to miss and
would produce subtle bugs when `base` is the manager's live configuration dict.

### Cross-Format Translation (`test_formats.py`)

The most interesting integration tests are in `TestCrossFormatTranslation`. They
simulate the exact workflow `ConfigurationManager.translate()` performs internally:
read with one factory's reader, write with another factory's writer. Five
combinations are covered (JSON↔YAML, JSON→ENV, YAML→ENV). These tests validate
that the Factory Method abstraction actually works end-to-end, not just that
`create_reader()` returns the right type.

### Custom Creator Registration

`TestRegisterCreator` defines a minimal `DummyCreator` for a `.dummy` extension
inline, registers it, and verifies that `load()` succeeds with the new format.
This tests the open/closed aspect of the design: adding a new format requires no
changes to the manager, only a new `FormatCreator` subclass.

A second test verifies that registering a creator for an already-known extension
(`.json`) replaces the old one, which is useful for overriding default behaviour
in tests or production integrations.

### Unicode

Unicode is tested at every level — adapters, readers, writers — using both
multi-language keys (`città`, `名前`) and values (`Roma`, `太郎`). The JSON adapter
test additionally asserts that `\u` escape sequences are **absent** from the
output, verifying that `ensure_ascii=False` is in effect. Without this check, a
correct-but-escaped output would still round-trip correctly and the bug would go
unnoticed.

---

## Fixtures

`conftest.py` provides three file-based fixtures built on pytest's `tmp_path`:

| Fixture | What it creates |
|---------|-----------------|
| `json_file` | A temporary `config.json` populated with `SAMPLE_JSON` |
| `yaml_file` | A temporary `config.yaml` populated with `SAMPLE_YAML` |
| `env_file` | A temporary `.env` populated with `SAMPLE_ENV` |

Edge-case inputs (invalid content, empty files, quoted values, etc.) are written
inline inside the tests that need them, keeping `conftest.py` minimal and focused
on the common happy-path setup.
