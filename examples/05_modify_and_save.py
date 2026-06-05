"""
05_modify_and_save.py — Modify configuration at runtime and persist changes.

This example demonstrates how to use `set()` to change values and
`save()` to write the entire configuration state to a new file.
"""

from proteus import ConfigurationManager


def main() -> None:
    config = ConfigurationManager()

    # 1. Load initial configuration
    config.load("examples/configs/app.yaml")
    print("--- 1. Initial State ---")
    print(f"App Name: {config.get('app_name')}")
    print(f"Port    : {config.get('server.port')}")

    # 2. Modify values at runtime
    print("\n--- 2. Modifying Values ---")
    config.set("app_name", "Proteus Powered App")
    config.set("server.port", 9000)

    # You can even create entirely new nested structures!
    config.set("meta.author", "Luca Di Leo")
    config.set("meta.version.major", 2)

    print(f"New App Name: {config.get('app_name')}")
    print(f"New Port    : {config.get('server.port')}")
    print(f"Meta Author : {config.get('meta.author')}")

    # 3. Save to a different format
    print("\n--- 3. Saving to TOML ---")
    output_path = "examples/output/updated_config.toml"
    config.save(output_path)
    print(f"Configuration persisted to: {output_path}")

    # 4. Verify the saved file
    with open(output_path, encoding="utf-8") as f:
        print("\n--- Saved TOML Content ---")
        print(f.read().strip())


if __name__ == "__main__":
    main()
