@echo off
REM One-click UI test runner (requires Appium + device/simulator)
set REPORT_DIR=.\Reports\ui-results
set OUTPUT_DIR=.\Reports\ui-report

echo === Starting Appium Server ===
start /b appium
timeout /t 3 /nobreak >nul

echo === Running UI Tests ===
pytest UI_Automation/Tests -v -n 0 --alluredir="%REPORT_DIR%"
set EXIT_CODE=%errorlevel%

echo === Stopping Appium Server ===
taskkill /f /im node.exe >nul 2>&1

echo === Generating Allure Report ===
allure generate "%REPORT_DIR%" -o "%OUTPUT_DIR%" --clean
allure open "%OUTPUT_DIR%"

exit /b %EXIT_CODE%
