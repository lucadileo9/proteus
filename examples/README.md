# Proteus Guided Tour

This directory contains a series of numbered examples designed to take you from basic usage to advanced architectural patterns in Proteus.

## 📂 Structure

- `01_basic_usage.py`: Loading single files and accessing values (Facade).
- `02_merge_configs.py`: Deep-merging multiple sources (Layering).
- `03_translate.py`: Cross-format translation (Full pattern collaboration).
- `configs/`: Source configuration files in various formats.
- `output/`: Generated files from the translation example.

---

## 🚦 How to run the examples

Run them directly from the project root using Python:

```bash
python examples/01_basic_usage.py
python examples/02_merge_configs.py
python examples/03_translate.py
```

---

## 🧠 What's happening behind the scenes?

### 01. Basic Usage (The Facade)
When you call `config.load("app.toml")`:
1. The **Facade** (`ConfigurationManager`) receives the request.
2. It uses a **Factory Method** to detect the `.toml` extension and pick the `TOMLFormatCreator`.
3. The creator provides a **Reader** that follows a **Template Method** (Validate → Read → Parse).
4. The **Adapter** (`TOMLAdapter`) uses `tomllib` to turn raw text into a Python `dict`.

### 02. Merging (Layering)
`config.merge()` is semantically equivalent to `load()`, but emphasizes the intent of adding an override layer.
- Proteus uses a **Recursive Deep Merge**: if both base and override contain a dictionary at the same key, it merges them instead of just overwriting the top-level key.
- This allows for powerful "Base configuration + Environment specific overrides" patterns.

### 03. Translation (Pattern Collaboration)
The `translate()` method demonstrates the true power of the design:
- It uses one **Reader** (e.g., YAML) to build the internal dictionary.
- It uses a different **Writer** (e.g., JSON) to serialize that dictionary to a new format.
- Because all formats are normalized into the same **Intermediate Representation (IR)**, you can convert between any two supported formats with zero data loss (types like integers and booleans are preserved!).

---

## 🛠️ Experimenting

Feel free to modify the files in `configs/` or add your own. Proteus is designed to be extensible—try adding a new format by following the [architecture documentation](../docs/architecture.md)!
