import asyncio
from pathlib import Path
from tools.webui.config import ALLURE_BIN, PROJECT_ROOT


async def generate_report(allure_results: Path, allure_report: Path) -> tuple[bool, str]:
    try:
        proc = await asyncio.create_subprocess_exec(
            ALLURE_BIN, "generate", str(allure_results),
            "-o", str(allure_report), "--clean",
            cwd=str(PROJECT_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
        if proc.returncode == 0:
            return True, str(allure_report / "index.html")
        return False, stderr.decode(errors="replace").strip()
    except asyncio.TimeoutError:
        return False, "Allure report generation timed out"
    except FileNotFoundError:
        return False, f"'{ALLURE_BIN}' command not found"
    except Exception as e:
        return False, str(e)
