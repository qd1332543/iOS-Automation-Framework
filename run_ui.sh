#!/bin/bash
# One-click UI test runner (requires Appium + device/simulator)
set -e

REPORT_DIR="./Reports/ui-results"
OUTPUT_DIR="./Reports/ui-report"

echo "=== Starting Appium Server ==="
appium &
APPIUM_PID=$!
sleep 3

echo "=== Running UI Tests ==="
pytest UI_Automation/Tests -v -n 0 --alluredir="$REPORT_DIR"
EXIT_CODE=$?

echo "=== Stopping Appium Server ==="
kill $APPIUM_PID

echo "=== Generating Allure Report ==="
allure generate "$REPORT_DIR" -o "$OUTPUT_DIR" --clean
allure open "$OUTPUT_DIR"

exit $EXIT_CODE
