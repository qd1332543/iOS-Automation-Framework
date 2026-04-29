import os
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).parent.parent.parent)).resolve()

WEBUI_HOST = os.getenv("WEBUI_HOST", "127.0.0.1")
WEBUI_PORT = int(os.getenv("WEBUI_PORT", "8000"))

AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-6")
AI_API_KEY = os.getenv("AI_API_KEY", "")

MAX_CONCURRENT_RUNS = int(os.getenv("MAX_CONCURRENT_RUNS", "1"))
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "1800"))
REPORTS_ROOT = PROJECT_ROOT / os.getenv("REPORTS_ROOT", "Reports/webui-runs")
ALLURE_BIN = os.getenv("ALLURE_BIN", "allure")

TEST_ENV = os.getenv("TEST_ENV", "dev")
APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
APP_PATH = os.getenv("APP_PATH", "")
IOS_DEVICE_NAME = os.getenv("IOS_DEVICE_NAME", "iPhone 15 Pro")
IOS_PLATFORM_VERSION = os.getenv("IOS_PLATFORM_VERSION", "17.2")
IOS_UDID = os.getenv("IOS_UDID", "")

WHITELIST_PATHS = [
    "README.md", "pytest.ini", "requirements.txt", "conftest.py",
    "run_api.bat", "run_api.sh", "run_ui.bat", "run_ui.sh",
    "API_Automation", "UI_Automation", "Performance/locust_scripts",
    "config/environments.yaml", "config/local.yml.example",
    "docs", "utils",
]

IGNORE_DIRS = {
    ".git", ".github", ".venv", "venv", "__pycache__",
    ".pytest_cache", "Reports", "allure-results", "node_modules",
    "tools",
}

SENSITIVE_FILES = {
    ".env", "config/local.yml", "local.yml",
}

SENSITIVE_EXTENSIONS = {".key", ".pem", ".p12", ".mobileprovision"}

MAX_FILE_SIZE = 200 * 1024  # 200KB
