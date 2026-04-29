import sys
import os
import asyncio
from pathlib import Path

# 确保项目根目录在 Python 路径中
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from tools.webui.config import PROJECT_ROOT, WEBUI_HOST, WEBUI_PORT

app = FastAPI(title="iOS-Automation-Framework WebUI")

@app.on_event("startup")
async def startup():
    from tools.webui.models import load_history
    load_history()

# ==================== Health ====================

@app.get("/api/health")
def health():
    return {"status": "ok"}

# ==================== Env ====================

@app.get("/api/env")
def env():
    from tools.webui.services.env_service import check_env
    return check_env()

# ==================== Files ====================

@app.get("/api/files")
def files():
    from tools.webui.services.file_service import get_file_tree
    return get_file_tree()

@app.get("/api/files/content")
def file_content(path: str):
    from tools.webui.services.file_service import get_file_content
    return get_file_content(path)

# ==================== Test Modules ====================

@app.get("/api/test-modules")
def test_modules():
    from tools.webui.services.env_service import check_env
    from tools.webui.services.run_service import get_modules
    return get_modules(check_env())

# ==================== Runs ====================

class RunRequest(BaseModel):
    module_id: str

@app.post("/api/runs", status_code=201)
async def create_run(req: RunRequest, background_tasks: BackgroundTasks):
    from tools.webui.services.run_service import TEST_MODULES, execute_run
    from tools.webui.models import create_run as _create
    from tools.webui.services.env_service import check_env

    if req.module_id not in TEST_MODULES:
        raise HTTPException(status_code=400, detail="Unknown module_id")

    m = TEST_MODULES[req.module_id]
    if m["type"] == "ui" and not check_env().get("ios_ui_runnable"):
        raise HTTPException(status_code=400, detail="iOS UI 自动化需要 macOS + Xcode + Appium")

    run = _create(req.module_id, m["pytest_args"])
    background_tasks.add_task(execute_run, run)
    return run.to_dict()

@app.get("/api/runs")
def list_runs():
    from tools.webui.models import list_runs as _list
    return [r.to_dict() for r in _list()]

@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    from tools.webui.models import get_run as _get
    run = _get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run.to_dict()

@app.get("/api/runs/{run_id}/events")
async def run_events(run_id: str):
    from tools.webui.models import get_run as _get
    run = _get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    async def generator():
        # 先发送已落盘的日志
        if run.log_file.exists():
            for line in run.log_file.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True):
                yield {"data": line.rstrip()}

        # 再实时推送新日志
        from tools.webui.models import RunStatus
        while run.status in (RunStatus.queued, RunStatus.running):
            try:
                line = await asyncio.wait_for(run._log_queue.get(), timeout=1.0)
                if line is None:
                    break
                yield {"data": line.rstrip()}
            except asyncio.TimeoutError:
                yield {"data": ""}  # keepalive

        yield {"event": "done", "data": run.status}

    return EventSourceResponse(generator())

@app.post("/api/runs/{run_id}/cancel")
async def cancel_run(run_id: str):
    from tools.webui.models import get_run as _get, RunStatus
    run = _get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if run.status not in (RunStatus.queued, RunStatus.running):
        raise HTTPException(status_code=400, detail="Run is not active")
    if run.process:
        try:
            run.process.kill()
        except Exception:
            pass
    run.status = RunStatus.cancelled
    return {"status": "cancelled"}

@app.get("/api/runs/{run_id}/report")
def run_report(run_id: str):
    from tools.webui.models import get_run as _get
    run = _get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if run.report_path:
        return {"available": True, "path": run.report_path}
    return {"available": False, "path": None}

# ==================== AI Chat ====================

class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat(req: ChatRequest):
    from tools.webui.services.ai_service import answer
    return await answer(req.question)

# ==================== Allure report static files ====================

from tools.webui.config import REPORTS_ROOT

@app.get("/reports/{run_id}/{rest_path:path}")
def serve_report(run_id: str, rest_path: str):
    target = (REPORTS_ROOT / run_id / "allure-report" / rest_path).resolve()
    try:
        target.relative_to(REPORTS_ROOT)
    except ValueError:
        raise HTTPException(status_code=403)
    if not target.exists():
        raise HTTPException(status_code=404)
    return FileResponse(str(target))

# ==================== Static ====================

_static = Path(__file__).parent / "static"
if _static.exists():
    app.mount("/static", StaticFiles(directory=str(_static)), name="static")

    @app.get("/")
    def index():
        return FileResponse(str(_static / "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tools.webui.app:app", host=WEBUI_HOST, port=WEBUI_PORT, reload=True)

