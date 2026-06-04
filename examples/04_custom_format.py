"""
04_custom_format.py — Extend Proteus with your own format.

This example shows how to add support for a completely new format
without modifying Proteus's core. We'll implement a simple pipe-separated
format (.txt) using only an Adapter and the `register_adapter` shortcut.
"""

from typing import Any, Dict

from proteus import BaseAdapter, ConfigurationManager


class PipeAdapter(BaseAdapter):
    """
    A custom adapter for a simple 'KEY|VALUE' text format.
    """

    def load(self, raw: str) -> Dict[str, Any]:
        """Parse pipe-separated lines into a dictionary."""
        data = {}
        for line in raw.strip().splitlines():
            if "|" in line:
                key, value = line.split("|", 1)
                data[key.strip()] = value.strip()
        return data

    def dump(self, data: Dict[str, Any]) -> str:
        """Serialize a dictionary into pipe-separated lines."""
        lines = [f"{k}|{v}" for k, v in data.items()]
        return "\n".join(lines) + "\n"


def main() -> None:
    config = ConfigurationManager()
    custom_file = "examples/configs/app.txt"

    print("--- 1. Registering Custom Adapter for .txt ---")
    # This single line handles the Factory Method, Reader, and Writer for you!
    config.register_adapter(extensions=[".txt"], adapter=PipeAdapter())

    print("\n--- 2. Loading Custom File ---")
    config.load(custom_file)
    print(f"Loaded App Name: {config.get('app_name')}")
    print(f"Loaded Version : {config.get('version')}")

    print("\n--- 3. Merging with YAML (Native + Custom) ---")
    # You can merge your custom format with native ones!
    config.merge("examples/configs/app.yaml")
    print(f"Combined DB Host: {config.get('database.host')}")

    print("\n--- 4. Translating Custom -> JSON ---")
    # You can even translate your format to any native Proteus format
    json_out = "examples/output/custom_to_json.json"
    config.translate(custom_file, json_out)
    print(f"Successfully translated {custom_file} to {json_out}")


if __name__ == "__main__":
    main()
