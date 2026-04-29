import sys
import asyncio
from datetime import datetime
from tools.webui.config import PROJECT_ROOT, DEFAULT_TIMEOUT_SECONDS, MAX_CONCURRENT_RUNS
from tools.webui.services.sanitize import sanitize

TEST_MODULES = {
    "api_all": {
        "name": "API 全量测试",
        "type": "api",
        "pytest_args": [sys.executable, "-m", "pytest", "API_Automation/cases", "-v"],
        "requires": ["pytest"],
    },
    "api_smoke": {
        "name": "API 冒烟测试",
        "type": "api",
        "pytest_args": [sys.executable, "-m", "pytest", "API_Automation/cases", "-v", "-m", "smoke"],
        "requires": ["pytest"],
    },
    "api_regression": {
        "name": "API 回归测试",
        "type": "api",
        "pytest_args": [sys.executable, "-m", "pytest", "API_Automation/cases", "-v", "-m", "regression"],
        "requires": ["pytest"],
    },
    "ui_all": {
        "name": "UI 全量测试",
        "type": "ui",
        "pytest_args": [sys.executable, "-m", "pytest", "UI_Automation/Tests", "-v", "-n", "0"],
        "requires": ["pytest", "appium", "xcode", "app_path"],
    },
    "ui_smoke": {
        "name": "UI 冒烟测试",
        "type": "ui",
        "pytest_args": [sys.executable, "-m", "pytest", "UI_Automation/Tests", "-v", "-n", "0", "-m", "smoke"],
        "requires": ["pytest", "appium", "xcode", "app_path"],
    },
}


def get_modules(env: dict) -> list[dict]:
    result = []
    for mid, m in TEST_MODULES.items():
        runnable = True
        reason = None
        if m["type"] == "ui" and not env.get("ios_ui_runnable"):
            runnable = False
            reason = "iOS UI 自动化需要 macOS + Xcode + Appium"
        result.append({
            "id": mid,
            "name": m["name"],
            "type": m["type"],
            "runnable": runnable,
            "disabled_reason": reason,
        })
    return result


# 并发控制
_semaphore: asyncio.Semaphore | None = None


def _get_semaphore() -> asyncio.Semaphore:
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(MAX_CONCURRENT_RUNS)
    return _semaphore


async def execute_run(run) -> None:
    """执行测试任务，管理生命周期"""
    from tools.webui.models import RunStatus
    from tools.webui.services.allure_service import generate_report

    sem = _get_semaphore()
    async with sem:
        run.status = RunStatus.running
        run.started_at = datetime.now()
        run.run_dir.mkdir(parents=True, exist_ok=True)
        run.allure_results.mkdir(parents=True, exist_ok=True)

        args = run.pytest_args + ["--alluredir", str(run.allure_results)]

        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                cwd=str(PROJECT_ROOT),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            run.process = proc

            with open(run.log_file, "w", encoding="utf-8") as f:
                async def _read():
                    while True:
                        line = await proc.stdout.readline()
                        if not line:
                            break
                        text = sanitize(line.decode(errors="replace"))
                        f.write(text)
                        f.flush()
                        await run._log_queue.put(text)

                await asyncio.wait_for(
                    asyncio.gather(_read(), proc.wait()),
                    timeout=DEFAULT_TIMEOUT_SECONDS,
                )

            run.exit_code = proc.returncode
            run.status = RunStatus.succeeded if proc.returncode == 0 else RunStatus.failed

        except asyncio.TimeoutError:
            run.status = RunStatus.timeout
            run.exit_code = -1
            if run.process:
                try:
                    run.process.kill()
                except Exception:
                    pass

        except asyncio.CancelledError:
            run.status = RunStatus.cancelled
            run.exit_code = -1
            if run.process:
                try:
                    run.process.kill()
                except Exception:
                    pass

        finally:
            run.finished_at = datetime.now()
            await run._log_queue.put(None)  # sentinel
            run.save_metadata()

        # 生成 Allure 报告（无论成功失败都尝试）
        ok, path = await generate_report(run.allure_results, run.allure_report)
        if ok:
            run.report_path = path
