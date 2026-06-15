# Proteus CLI Demo Script (Windows PowerShell)
# This script demonstrates the full power of the Proteus Command Line Interface.
# It assumes you have installed proteus-config (pip install -e .)

# 0. Setup environment
$env:PYTHONPATH = "src"
$CONFIG_DIR = "examples/configs"
$OUTPUT_DIR = "examples/output"

Write-Host "--- Proteus CLI Demo Start ---" -ForegroundColor Cyan

# 1. Translate: Convert an ENV file to JSON
Write-Host "`n1. Translating ENV to JSON..." -ForegroundColor Yellow
Write-Host "Command: proteus translate '$CONFIG_DIR/app.env' '$OUTPUT_DIR/cli_demo.json'"
python -m proteus.cli translate "$CONFIG_DIR/app.env" "$OUTPUT_DIR/cli_demo.json"
Write-Host "Done! Checked $OUTPUT_DIR/cli_demo.json"
Read-Host -Prompt "Press Enter to continue to the next step..."

# 2. Set: Modify a value in the newly created JSON
Write-Host "`n2. Modifying a value (app.debug = true)..." -ForegroundColor Yellow
Write-Host "Command: proteus set '$OUTPUT_DIR/cli_demo.json' 'app.debug' 'true'"
python -m proteus.cli set "$OUTPUT_DIR/cli_demo.json" "app.debug" "true"
Read-Host -Prompt "Press Enter to continue to the next step..."

# 3. Get: Read a specific key back (with casting)
Write-Host "`n3. Reading the value back as a boolean:" -ForegroundColor Yellow
Write-Host "Command: proteus get '$OUTPUT_DIR/cli_demo.json' 'app.debug' --cast bool"
$DEBUG_VAL = python -m proteus.cli get "$OUTPUT_DIR/cli_demo.json" "app.debug" --cast bool
Write-Host "DEBUG value is: $DEBUG_VAL"
Read-Host -Prompt "Press Enter to continue to the next step..."

# 4. Merge: Combine multiple files into a final TOML
Write-Host "`n4. Merging JSON and YAML into a final TOML file..." -ForegroundColor Yellow
Write-Host "Command: proteus merge '$OUTPUT_DIR/cli_demo.json' '$CONFIG_DIR/app.yaml' --out '$OUTPUT_DIR/cli_merged.toml'"
python -m proteus.cli merge "$OUTPUT_DIR/cli_demo.json" "$CONFIG_DIR/app.yaml" --out "$OUTPUT_DIR/cli_merged.toml"
Read-Host -Prompt "Press Enter to continue to the next step..."

# 5. View: Inspect the final merged configuration as JSON
Write-Host "`n5. Inspecting the final merged configuration:" -ForegroundColor Yellow
Write-Host "Command: proteus view '$OUTPUT_DIR/cli_merged.toml'"
python -m proteus.cli view "$OUTPUT_DIR/cli_merged.toml"
Read-Host -Prompt "Press Enter to continue to the next step..."

# 6. List-Files: Show absolute paths of used files
Write-Host "`n6. Auditing loaded files (Absolute paths):" -ForegroundColor Yellow
Write-Host "Command: proteus list-files '$OUTPUT_DIR/cli_merged.toml'"
python -m proteus.cli list-files "$OUTPUT_DIR/cli_merged.toml"

Write-Host "`n--- Demo Completed Successfully! ---" -ForegroundColor Green
