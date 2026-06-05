"""
02_merge_configs.py — Deep-merge a base config with environment overrides.

This example demonstrates the **Deep Merge** logic and how Proteus handles
multi-source configurations (e.g., base settings + production overrides).

Behind the scenes:
- **Deep Merge**: If both base and override values are dictionaries, they are merged.
- **Priority**: Files loaded later overwrite values from files loaded earlier.
"""

from proteus import ConfigurationManager


def main() -> None:
    config = ConfigurationManager()

    print("--- 1. Loading Base YAML ---")
    config.load("examples/configs/app.yaml")
    print(f"Initial DB host: {config.get('database.host')}")  # localhost
    print(f"Initial DB port: {config.get('database.port')}")  # 5432
    print(f"Initial Log level: {config.get('logging.level')}")  # INFO

    print("\n--- 2. Merging Production Overrides (YAML) ---")
    config.merge("examples/configs/production.yaml")
    # host is updated, port (not in production.yaml) is preserved
    print(f"Updated DB host : {config.get('database.host')}")  # prod-db.example.com
    print(f"Preserved DB port: {config.get('database.port')}")  # 5432
    print(f"Updated Log level : {config.get('logging.level')}")  # WARNING

    print("\n--- 3. Merging ENV Overrides (.env) ---")
    # ENV format typically uses __ for nesting
    config.merge("examples/configs/app.env")
    # Values from .env now win
    print(f"Final App Name: {config.get('APP_NAME')}")
    print(f"Final DB User : {config.get('DATABASE.USER')}")
    print(f"Final DB port : {config.get('DATABASE.PORT')}")

    config.reset()


if __name__ == "__main__":
    main()
