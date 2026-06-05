#!/bin/bash
# Proteus CLI Demo Script (Linux/macOS)
# This script demonstrates the full power of the Proteus Command Line Interface.

export PYTHONPATH="src"
CONFIG_DIR="examples/configs"
OUTPUT_DIR="examples/output"

echo -e "\033[0;36m--- Proteus CLI Demo Start ---\033[0m"

# 1. Translate
echo -e "\n\033[0;33m1. Translating ENV to JSON...\033[0m"
python3 -m proteus.cli translate "$CONFIG_DIR/app.env" "$OUTPUT_DIR/cli_demo.json"

# 2. Set
echo -e "\n\033[0;33m2. Modifying a value (app.debug = true)...\033[0m"
python3 -m proteus.cli set "$OUTPUT_DIR/cli_demo.json" "app.debug" "true"

# 3. Get
echo -e "\n\033[0;33m3. Reading the value back as a boolean:\033[0m"
DEBUG_VAL=$(python3 -m proteus.cli get "$OUTPUT_DIR/cli_demo.json" "app.debug" --cast bool)
echo "DEBUG value is: $DEBUG_VAL"

# 4. Merge
echo -e "\n\033[0;33m4. Merging JSON and YAML into a final TOML file...\033[0m"
python3 -m proteus.cli merge "$OUTPUT_DIR/cli_demo.json" "$CONFIG_DIR/app.yaml" --out "$OUTPUT_DIR/cli_merged.toml"

# 5. View
echo -e "\n\033[0;33m5. Inspecting the final merged configuration:\033[0m"
python3 -m proteus.cli view "$OUTPUT_DIR/cli_merged.toml"

# 6. List-Files
echo -e "\n\033[0;33m6. Auditing loaded files (Absolute paths):\033[0m"
python3 -m proteus.cli list-files "$OUTPUT_DIR/cli_merged.toml"

echo -e "\n\033[0;32m--- Demo Completed Successfully! ---\033[0m"
