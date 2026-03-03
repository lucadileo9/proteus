"""
basic_usage.py — Load a configuration file and access values.

Run from the project root:
    python examples/basic_usage.py
"""

from proteus import ConfigurationManager

def main():
    config = ConfigurationManager()

    # Load a YAML configuration file
    config.load("config_examples/app.yaml")

    # Access values with dot-notation
    print("App name :", config.get("app_name"))
    print("DB host  :", config.get("database.host"))
    print("DB port  :", config.get("database.port"))
    print("Log level:", config.get("logging.level"))

    # Access a missing key with a default
    print("Timeout  :", config.get("server.timeout", 30))

    # Dump the entire configuration
    print("\nFull config:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")

    # Clean up singleton state for next example run
    config.reset()
    ConfigurationManager._destroy()


if __name__ == "__main__":
    main()
