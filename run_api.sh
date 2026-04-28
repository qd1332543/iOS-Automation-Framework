#!/bin/bash
# One-click API test runner
set -e

REPORT_DIR="./Reports/api-results"
OUTPUT_DIR="./Reports/api-report"

echo "=== Running API Tests ==="
pytest API_Automation/cases -v --alluredir="$REPORT_DIR"

echo "=== Generating Allure Report ==="
allure generate "$REPORT_DIR" -o "$OUTPUT_DIR" --clean
allure open "$OUTPUT_DIR"
