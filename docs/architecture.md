# Architecture

> Proteus is built around five GoF design patterns arranged in a deliberate stack. Each layer has a single responsibility and delegates down to the next.

## Pattern Stack

```
┌─────────────────────────────────────────────┐
│  Optional Singleton + Facade (ConfigurationManager) │  ← single entry point
├─────────────────────────────────────────────┤
│  Factory Method      (FormatCreator)        │  ← selects reader/writer
├─────────────────────────────────────────────┤
│  Template Method     (BaseReader/BaseWriter)│  ← defines the algorithm
├─────────────────────────────────────────────┤
│  Adapter             (BaseAdapter)          │  ← wraps third-party libs
└─────────────────────────────────────────────┘
```

| Pattern | Class | Responsibility |
|---|---|---|
| **Singleton** | `ConfigurationManager.instance()` | One global instance, thread-safe |
| **Facade** | `ConfigurationManager` | Simple API over the full pattern stack |
| **Factory Method** | `FormatCreator` and subclasses | Create the right Reader/Writer pair |
| **Template Method** | `BaseReader`, `BaseWriter` | Fixed algorithm, format-specific steps |
| **Adapter** | `BaseAdapter` and subclasses | Wrap `json`, `pyyaml`, `tomllib`, `dotenv` |

---

## Component Map

```mermaid
flowchart TD
    Client --> CM[ConfigurationManager Facade]
    Client --> S[ConfigurationManager.instance() Optional Singleton]

    CM --> FC{FormatCreator Factory Method}
    S --> FC

    FC --> JC[JSONFormatCreator]
    FC --> YC[YAMLFormatCreator]
    FC --> TC[TOMLFormatCreator]
    FC --> EC[EnvFormatCreator]

    JC --> JR[JSONReader] & JW[JSONWriter]
    YC --> YR[YAMLReader] & YW[YAMLWriter]
    TC --> TR[TOMLReader] & TW[TOMLWriter]
    EC --> ER[EnvReader] & EW[EnvWriter]

    JR & JW --> JA[JSONAdapter wraps: json]
    YR & YW --> YA[YAMLAdapter wraps: pyyaml]
    TR & TW --> TA[TOMLAdapter wraps: tomllib/tomli-w]
    ER & EW --> EA[EnvAdapter wraps: python-dotenv]
```

### Factory Method: FormatCreator
`ConfigurationManager` uses the Factory Method pattern to select the appropriate `FormatCreator` based on file extension. Each `FormatCreator` knows how to create its own Reader and Writer, which in turn use Adapters to interact with third-party libraries.

```mermaid
    classDiagram
    class FormatCreator {
        <<Abstract — Creator>>
        +create_reader()* BaseReader
        +create_writer()* BaseWriter
        +get_extensions()* List~str~
    }

    class JSONFormatCreator {
        <<Concrete Creator>>
        +create_reader() JSONReader
        +create_writer() JSONWriter
        +get_extensions() List~str~
    }

    class YAMLFormatCreator {
        <<Concrete Creator>>
        +create_reader() YAMLReader
        +create_writer() YAMLWriter
        +get_extensions() List~str~
    }

    class TOMLFormatCreator {
        <<Concrete Creator>>
        +create_reader() TOMLReader
        +create_writer() TOMLWriter
        +get_extensions() List~str~
    }

    class EnvFormatCreator {
        <<Concrete Creator>>
        +create_reader() EnvReader
        +create_writer() EnvWriter
        +get_extensions() List~str~
    }

    FormatCreator <|-- JSONFormatCreator
    FormatCreator <|-- YAMLFormatCreator
    FormatCreator <|-- TOMLFormatCreator
    FormatCreator <|-- EnvFormatCreator

    JSONFormatCreator ..> JSONReader : creates
    JSONFormatCreator ..> JSONWriter : creates
    YAMLFormatCreator ..> YAMLReader : creates
    YAMLFormatCreator ..> YAMLWriter : creates
    TOMLFormatCreator ..> TOMLReader : creates
    TOMLFormatCreator ..> TOMLWriter : creates
    EnvFormatCreator ..> EnvReader : creates
    EnvFormatCreator ..> EnvWriter : creates

    note for FormatCreator "FACTORY METHOD (GoF):
    create_reader() and create_writer()
    are the two abstract factory methods.
    Purpose: couple the Reader+Writer
    of the same format. The Manager
    only knows FormatCreator (DIP)."
```

### Template Method: BaseReader/BaseWriter
`BaseReader` and `BaseWriter` define the skeleton of the parsing and writing algorithms. The concrete Readers/Writers implement the format-specific steps, while the Base classes handle common logic like file I/O and error handling.

```mermaid
classDiagram
    class BaseReader {
        <<Abstract — Template Method>>
        +parse(filepath : str) Dict
        #_validate(filepath : str) void
        #_read_file(filepath : str) str
        #_parse_content(raw : str)* Dict
        #_normalize_data(data : Dict) Dict
    }

    class JSONReader {
        -_adapter : JSONAdapter
        #_parse_content(raw : str) Dict
    }

    class TOMLReader {
        -_adapter : TOMLAdapter
        #_parse_content(raw : str) Dict
    }

    class BaseWriter {
        <<Abstract — Template Method>>
        +write(data : Dict, filepath : str) void
        #_validate(data : Dict, filepath : str) void
        #_serialize(data : Dict)* str
        #_write_file(content : str, filepath : str) void
    }

    class JSONWriter {
        -_adapter : JSONAdapter
        #_serialize(data : Dict) str
    }

    class TOMLWriter {
        -_adapter : TOMLAdapter
        #_serialize(data : Dict) str
    }

    BaseReader <|-- JSONReader
    BaseReader <|-- YAMLReader
    BaseReader <|-- TOMLReader
    BaseReader <|-- EnvReader
    BaseWriter <|-- JSONWriter
    BaseWriter <|-- YAMLWriter
    BaseWriter <|-- TOMLWriter
    BaseWriter <|-- EnvWriter

    note for BaseReader "Template Method: parse()
    1. _validate()       ← common
    2. _read_file()      ← common
    3. _parse_content()  ← VARIABLE (abstract)
    4. _normalize_data() ← common
    The variable step delegates to the Adapter."

    note for BaseWriter "Template Method: write()
    1. _validate()   ← common
    2. _serialize()  ← VARIABLE (abstract)
    3. _write_file() ← common
    The variable step delegates to the Adapter."
```

### Adapter: BaseAdapter
The Adapters wrap the third-party libraries and expose a consistent interface to the Readers/Writers. This isolates external dependencies and allows for easier maintenance or swapping of libraries in the future.

```mermaid
%%{ init: {"layout": "elk"} }%%
classDiagram
    class BaseAdapter {
        <<Abstract — Target>>
        +load(raw : str)* Dict
        +dump(data : Dict)* str
    }

    class JSONAdapter {
        <<Adapter>>
        +load(raw : str) Dict
        +dump(data : Dict) str
    }

    class YAMLAdapter {
        <<Adapter>>
        +load(raw : str) Dict
        +dump(data : Dict) str
    }

    class TOMLAdapter {
        <<Adapter>>
        +load(raw : str) Dict
        +dump(data : Dict) str
    }

    class EnvAdapter {
        <<Adapter>>
        +load(raw : str) Dict
        +dump(data : Dict) str
    }


    class json_lib {
        <<Adaptee — stdlib>>
        +loads(s : str) Any
        +dumps(obj : Any) str
    }

    class yaml_lib {
        <<Adaptee — PyYAML>>
        +safe_load(stream) Any
        +dump(data) str
    }

    class toml_lib {
        <<Adaptee — tomllib/tomli>>
        +loads(s : str) Dict
    }

    class toml_w_lib {
        <<Adaptee — tomli-w>>
        +dumps(d : Dict) str
    }

    class dotenv_lib {
        <<Adaptee — python-dotenv>>
        +dotenv_values(stream) OrderedDict
    }


    BaseAdapter <|-- JSONAdapter
    BaseAdapter <|-- YAMLAdapter
    BaseAdapter <|-- TOMLAdapter
    BaseAdapter <|-- EnvAdapter

    JSONAdapter ..> json_lib : wraps
    YAMLAdapter ..> yaml_lib : wraps
    TOMLAdapter ..> toml_lib : wraps
    TOMLAdapter ..> toml_w_lib : wraps
    EnvAdapter ..> dotenv_lib : wraps

    note for BaseAdapter "TARGET: uniform interface
    load() → raw text → Dict (IR)
    dump() → Dict (IR) → raw text"
    note for JSONAdapter "ADAPTER: translates json.loads/dumps
    to the Target interface.
    Shared by JSONReader and JSONWriter."
    note for json_lib "ADAPTEE: external interface
    incompatible with the system IR."
```


---

## Intermediate Representation (IR)

All formats share a single common structure in memory: a plain Python `Dict[str, Any]`. This is what enables format-agnostic merging and translation.

```
.json file  ──┐
.yaml file  ──┤
.toml file  ──┤─── Reader.parse() ──► Dict[str, Any]  ──► Writer.write() ──► file
.env file   ──┘          (IR)
```

### Nested formats (JSON, YAML)

Both JSON and YAML map naturally to nested Python dicts:

```json
// config.json
{
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "app": {
    "debug": true
  }
}
```

```python
# IR in memory — identical regardless of whether source was JSON or YAML
{
    "database": {"host": "localhost", "port": 5432},
    "app": {"debug": True},
}
```

### Flat format (ENV)

The `.env` format has no native nesting. To maintain a unified experience, Proteus uses the `__` separator convention:
- **On Write**: Nested dictionaries are flattened (e.g. `{"DB": {"HOST": "..."}}` → `DB__HOST=...`).
- **On Read**: Flat keys are automatically **unflattened** back into dictionaries.

This ensures that `config.get("DB.HOST")` works regardless of the source format.

### Accessing the IR

`ConfigurationManager.get()` navigates the IR using **dot-notation**:

```python
config.get("database.host")   # → "localhost"  (nested key)
config.get("DATABASE__HOST")  # → "localhost"  (flat ENV key)
config.get("missing", "N/A") # → "N/A"        (default)
```

---

## Data Flow: `load()` / `merge()`

```mermaid
sequenceDiagram
    actor Client
    participant CM as ConfigurationManager<br/>(Singleton + Facade)
    participant FC as YAMLFormatCreator<br/>(Factory Method)
    participant R as YAMLReader<br/>(Template Method)
    participant A as YAMLAdapter<br/>(Adapter)
    participant LIB as yaml<br/>(Adaptee)
    participant FS as FileSystem

    Client->>+CM: ConfigurationManager()
    Note over CM: __new__() double-check<br/>locking → returns<br/>the same instance (Singleton)
    CM-->>-Client: unique instance

    Client->>+CM: load("config.yaml")
    Note over CM: Facade hides everything<br/>that follows

    CM->>CM: _get_creator(".yaml")
    CM->>+FC: create_reader()
    FC-->>-CM: YAMLReader

    CM->>+R: parse("config.yaml")
    Note over R: Template Method:<br/>4 fixed steps

    R->>R: 1. _validate("config.yaml")
    R->>+FS: exists?
    FS-->>-R: true

    R->>R: 2. _read_file("config.yaml")
    R->>+FS: read_text()
    FS-->>-R: "database: host: localhost"

    R->>R: 3. _parse_content(raw)
    R->>+A: load(raw)
    A->>+LIB: safe_load(raw)
    LIB-->>-A: {database: {host: localhost}}
    A-->>-R: Dict (IR)

    R->>R: 4. _normalize_data(dict)
    R-->>-CM: Dict (IR)

    CM->>CM: _deep_merge(_config, new_config)
    CM-->>-Client: void
```

---

## Data Flow: `get()`

`get(key, default)` retrieves values from the internal configuration dictionary (IR). It supports dot-notation for navigating nested structures, handling missing keys safely by returning the provided default.

```mermaid
sequenceDiagram
    actor Client
    participant CM as ConfigurationManager<br/>(Singleton + Facade)
    participant IR as _config<br/>(Dict)

    Note over Client,IR: Scenario 1: Deep Nested Lookup (JSON/YAML)
    Client->>+CM: get("app.server.port", 8080)
    Note over CM: Split by ".": ["app", "server", "port"]
    CM->>+IR: lookup "app"
    IR-->>-CM: {"server": {"port": 3000}}
    CM->>+IR: lookup "server"
    IR-->>-CM: {"port": 3000}
    CM->>+IR: lookup "port"
    IR-->>-CM: 3000
    CM-->>-Client: 3000

    Note over Client,IR: Scenario 2: Flat Lookup (ENV)
    Client->>+CM: get("APP__SERVER__PORT", 8080)
    Note over CM: Split by ".": ["APP__SERVER__PORT"]<br/>(No dots to split)
    CM->>+IR: lookup "APP__SERVER__PORT"
    IR-->>-CM: "3000"
    CM-->>-Client: "3000"

    Note over Client,IR: Scenario 3: Missing Key with Default
    Client->>+CM: get("database.password", "N/A")
    Note over CM: Split by ".": ["database", "password"]
    CM->>+IR: lookup "database"
    IR-->>-CM: KeyError
    Note over CM: Traversal stops, catches error
    CM-->>-Client: "N/A" (Default returned)
```

---

## Data Flow: `translate()`

`translate(src, dst)` selects **two independent creators**: one for the source file extension, one for the destination. Each creator produces its own Reader or Writer. There is no shared state between them.

```
translate("config.yaml", "config.json")
        └──────────────┘ └─────────────┘
        ↓ extension: .yaml          ↓ extension: .json
    YAMLFormatCreator            JSONFormatCreator
    ↓ create_reader()            ↓ create_writer()
    YAMLReader                   JSONWriter
```

```mermaid
sequenceDiagram
    actor Client
    participant CM as ConfigurationManager<br/>(Singleton + Facade)
    participant FC_IN as YAMLFormatCreator<br/>(Factory)
    participant R as YAMLReader<br/>(Template Method)
    participant A_IN as YAMLAdapter<br/>(Adapter)
    participant YAML as yaml (Adaptee)
    participant FC_OUT as JSONFormatCreator<br/>(Factory)
    participant W as JSONWriter<br/>(Template Method)
    participant A_OUT as JSONAdapter<br/>(Adapter)
    participant JSON as json (Adaptee)

    Client->>+CM: translate("config.yaml", "output.json")

    Note over CM: Phase 1 — Read

    CM->>CM: _get_creator(".yaml")
    CM->>+FC_IN: create_reader()
    FC_IN-->>-CM: YAMLReader

    CM->>+R: parse("config.yaml")
    R->>R: _validate() + _read_file()
    R->>R: _parse_content(raw)
    R->>+A_IN: load(raw)
    A_IN->>+YAML: safe_load(raw)
    YAML-->>-A_IN: Any
    A_IN-->>-R: Dict (IR)
    R->>R: _normalize_data()
    R-->>-CM: Dict (IR)

    Note over CM: Phase 2 — Write

    CM->>CM: _get_creator(".json")
    CM->>+FC_OUT: create_writer()
    FC_OUT-->>-CM: JSONWriter

    CM->>+W: write(dict, "output.json")
    W->>W: _validate()
    W->>W: _serialize(data)
    W->>+A_OUT: dump(dict)
    A_OUT->>+JSON: dumps(dict)
    JSON-->>-A_OUT: str
    A_OUT-->>-W: str
    W->>W: _write_file()
    W-->>-CM: void

    CM-->>-Client: void (file written)
```


`translate()` does **not** touch `self._config` — it is a pure file-to-file conversion.

---

## Deep-Merge Semantics

When loading multiple files, nested dicts are merged recursively. Scalar values from the later file always win:

```python
# base.yaml          # prod.yaml          # result
database:            database:            database:
  host: localhost       host: prod-db        host: prod-db   ← overridden
  port: 5432                                 port: 5432      ← preserved
```

---

## Extensibility

New formats can be added at runtime without modifying existing code (Open/Closed Principle):

```python
mgr = ConfigurationManager()
mgr.register_creator(TOMLFormatCreator())  # plugged in dynamically
mgr.load("config.toml")                   # works immediately
```

A custom creator only needs to implement three methods: `create_reader()`, `create_writer()`, and `get_extensions()`. Everything else — Template Method, Adapter wiring — is inherited from the base classes.
