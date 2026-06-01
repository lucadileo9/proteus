"""
01_basic_usage.py — Comprehensive loading example for all supported formats.

This script demonstrates how to load and access data from every format
Proteus supports: YAML, JSON, TOML, and ENV.
"""

from proteus import ConfigurationManager


def main() -> None:
    # We use a fresh manager for each format to show them clearly
    config = ConfigurationManager()

    print("--- 1. YAML Loading ---")
    config.load("examples/configs/app.yaml")
    print(f"App name: {config.get('app_name')}")
    print(f"Host    : {config.get('server.host')}")
    config.reset()

    print("\n--- 2. JSON Loading ---")
    config.load("examples/configs/app.json")
    print(f"Version : {config.get('version')}")
    print(f"Port    : {config.get('server.port')}")
    config.reset()

    print("\n--- 3. TOML Loading (Strongly Typed) ---")
    config.load("examples/configs/app.toml")
    # TOML preserves types like integers and booleans nativly
    port = config.get("server.port")
    print(f"Port    : {port} (Type: {type(port).__name__})")
    config.reset()

    print("\n--- 4. ENV Loading (Flat to Nested) ---")
    config.load("examples/configs/app.env")
    # Proteus supports standard ENV nesting using __ separator
    print(f"DB Host : {config.get('DATABASE__HOST')}")
    print(f"DB Name : {config.get('DATABASE__NAME')}")

    print("\n✅ All formats loaded successfully using the same Facade API!")


if __name__ == "__main__":
    main()
