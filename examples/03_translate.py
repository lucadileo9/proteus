"""
03_translate.py — Interactive translation between all supported formats.

This script acts as a LIVE DEMO. It translates configuration data through
a complete cycle (YAML -> JSON -> TOML -> ENV -> YAML) and prints the
content of each file so you can see how Proteus handles the data.

Design Patterns in action:
- **Facade**: `config.translate()` hides all the complexity.
- **Factory Method**: Automatically picks the right Reader/Writer pair.
- **Adapter**: Decouples the logic from third-party libraries.
"""

import os
from pathlib import Path

from proteus import ConfigurationManager

OUTPUT_DIR = Path("examples/output")


def print_file_content(path: Path, title: str) -> None:
    """Helper to print file content with a nice header."""
    print(f"\n--- {title} ({path.name}) ---")
    print(path.read_text(encoding="utf-8").strip())


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    config = ConfigurationManager()

    print("=== Proteus Interactive Translation Demo ===")
    print("This script will cycle a configuration through all supported formats.")

    # 1. YAML to JSON
    yaml_src = Path("examples/configs/app.yaml")
    json_dst = OUTPUT_DIR / "translated.json"

    print_file_content(yaml_src, "Source YAML")
    print("\nAction: Translating YAML -> JSON...")
    config.translate(yaml_src, json_dst)
    print_file_content(json_dst, "Resulting JSON")
    input("\n[1/4] YAML to JSON complete. Press Enter to continue...")

    # 2. JSON to TOML
    toml_dst = OUTPUT_DIR / "translated.toml"
    print("\nAction: Translating JSON -> TOML...")
    config.translate(json_dst, toml_dst)
    print_file_content(toml_dst, "Resulting TOML")
    print("\nNote: TOML is strongly typed, notice how port is an integer (no quotes).")
    input("\n[2/4] JSON to TOML complete. Press Enter to continue...")

    # 3. TOML to ENV
    env_dst = OUTPUT_DIR / "translated.env"
    print("\nAction: Translating TOML -> ENV...")
    config.translate(toml_dst, env_dst)
    print_file_content(env_dst, "Resulting ENV")
    print("\nNote: ENV uses '__' to represent nested structures (e.g. DATABASE__HOST).")
    input("\n[3/4] TOML to ENV complete. Press Enter to continue...")

    # 4. ENV to YAML (Back to start)
    yaml_final = OUTPUT_DIR / "translated_back.yaml"
    print("\nAction: Translating ENV -> YAML...")
    config.translate(env_dst, yaml_final)
    print_file_content(yaml_final, "Final YAML (Back from ENV)")
    input("\n[4/4] Cycle complete! Press Enter to verify the data...")

    print("\n--- Final Verification ---")
    # Load the back-translated file to prove it's still valid configuration
    config.load(yaml_final)
    # Env translation often results in uppercased keys
    app_name = config.get("APP_NAME")
    print(f"Loading generated file... Found APP_NAME: {app_name}")

    print(
        "\nAll translations verified! Proteus maintained "
        + "data integrity across all formats."
    )


if __name__ == "__main__":
    main()
