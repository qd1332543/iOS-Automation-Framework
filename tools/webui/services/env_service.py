import os
import sys
import platform
import shutil
import subprocess
from tools.webui.config import APPIUM_URL, APP_PATH, ALLURE_BIN


def _run(cmd: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


def check_env() -> dict:
    plat = platform.system()  # Windows / Darwin / Linux
    is_mac = plat == "Darwin"

    # Python
    py_ver = sys.version.split()[0]

    # pytest
    ok_pytest, pytest_out = _run(["pytest", "--version"])

    # allure
    ok_allure, allure_out = _run([ALLURE_BIN, "--version"])

    # appium (ping server)
    ok_appium = False
    appium_msg = "Appium server unavailable"
    try:
        import urllib.request
        urllib.request.urlopen(APPIUM_URL + "/status", timeout=3)
        ok_appium = True
        appium_msg = APPIUM_URL
    except Exception:
        pass

    # xcode (macOS only)
    ok_xcode = False
    xcode_msg = "Xcode requires macOS"
    if is_mac:
        ok_xcode, xcode_msg = _run(["xcodebuild", "-version"])

    ios_ui_runnable = is_mac and ok_appium and ok_xcode and bool(APP_PATH)
    api_runnable = ok_pytest

    return {
        "platform": plat,
        "python": {"ok": True, "version": py_ver},
        "pytest": {"ok": ok_pytest, "version": pytest_out if ok_pytest else None, "message": None if ok_pytest else pytest_out},
        "allure": {"ok": ok_allure, "version": allure_out if ok_allure else None, "message": None if ok_allure else allure_out},
        "appium": {"ok": ok_appium, "message": appium_msg},
        "xcode": {"ok": ok_xcode, "message": xcode_msg},
        "ios_ui_runnable": ios_ui_runnable,
        "api_runnable": api_runnable,
    }
