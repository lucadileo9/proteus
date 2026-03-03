"""
translate.py — Convert a configuration file between formats.

Run from the project root:
    python examples/translate.py
"""

import os

from proteus import ConfigurationManager

OUTPUT_DIR = "config_examples/output"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    config = ConfigurationManager()

    # YAML → JSON
    json_out = os.path.join(OUTPUT_DIR, "app.json")
    config.translate("config_examples/app.yaml", json_out)
    print("=== YAML → JSON ===")
    print("This is the configuration in YAML file format:")
    print(open("config_examples/app.yaml", encoding="utf-8").read())
    print("\nThis is the same configuration translated to JSON format:")
    print(open(json_out, encoding="utf-8").read())
    input("\nPress Enter to continue to the next translation...")

    # JSON → ENV
    env_out = os.path.join(OUTPUT_DIR, "app.env")
    config.translate(json_out, env_out)
    print("=== JSON → ENV ===")
    print("This is the configuration in JSON file format:")
    print(open(json_out, encoding="utf-8").read())
    print("\nThis is the same configuration translated to ENV format\n(KEY=VALUE pairs):")
    print(open(env_out, encoding="utf-8").read())
    input("\nPress Enter to continue to the next translation...")

    # ENV → YAML
    yaml_out = os.path.join(OUTPUT_DIR, "app_from_env.yaml")
    config.translate(env_out, yaml_out)
    print("=== ENV → YAML ===")
    print("This is the configuration in ENV file format (KEY=VALUE pairs):")
    print(open(env_out, encoding="utf-8").read())
    print("\nThis is the same configuration translated back to YAML format:")
    print(open(yaml_out, encoding="utf-8").read())
    input("\nPress Enter to continue to the next translation...")
    
    # Clean up singleton state
    config.reset()
    ConfigurationManager._destroy()


if __name__ == "__main__":
    main()
