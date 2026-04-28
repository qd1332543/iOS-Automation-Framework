@echo off
REM One-click API test runner
set REPORT_DIR=.\Reports\api-results
set OUTPUT_DIR=.\Reports\api-report

echo === Running API Tests ===
pytest API_Automation/cases -v --alluredir="%REPORT_DIR%"
if errorlevel 1 goto :error

echo === Generating Allure Report ===
allure generate "%REPORT_DIR%" -o "%OUTPUT_DIR%" --clean
allure open "%OUTPUT_DIR%"
goto :end

:error
echo Tests failed.
exit /b 1

:end
