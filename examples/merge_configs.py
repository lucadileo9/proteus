"""
merge_configs.py — Deep-merge a base config with production overrides.

Run from the project root:
    python examples/merge_configs.py
"""

from proteus import ConfigurationManager


def main() -> None:
    config = ConfigurationManager()

    # Load base configuration
    config.load("config_examples/app.yaml")
    print("=== After loading app.yaml ===")
    print("DB host:", config.get("database.host"))
    print("DB pass:", config.get("database.password"))
    print("Log file:", config.get("logging.file"))

    # Merge production overrides on top (values in production.yaml win)
    config.merge("config_examples/production.yaml")
    print("\n=== After merging production.yaml ===")
    print("DB host:", config.get("database.host"))
    print("DB pass:", config.get("database.password"))
    print("Log file:", config.get("logging.file"))

    # Keys only in base are preserved
    print("\nDB port (only in base):", config.get("database.port"))

    # Clean up singleton state
    config.reset()
    ConfigurationManager._destroy()


if __name__ == "__main__":
    main()
