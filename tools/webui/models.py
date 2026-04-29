import asyncio
import json
import sys
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from tools.webui.config import PROJECT_ROOT, REPORTS_ROOT, DEFAULT_TIMEOUT_SECONDS


class RunStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"
    timeout = "timeout"


class Run:
    def __init__(self, module_id: str, pytest_args: list[str]):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.run_id = f"{ts}-{module_id}-{uuid4().hex[:6]}"
        self.module_id = module_id
        self.pytest_args = pytest_args
        self.status = RunStatus.queued
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None
        self.exit_code: Optional[int] = None
        self.report_path: Optional[str] = None
        self.run_dir = REPORTS_ROOT / self.run_id
        self.log_file = self.run_dir / "logs.txt"
        self.allure_results = self.run_dir / "allure-results"
        self.allure_report = self.run_dir / "allure-report"
        self.process: Optional[asyncio.subprocess.Process] = None
        self._log_queue: asyncio.Queue = asyncio.Queue()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "module_id": self.module_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "exit_code": self.exit_code,
            "report_path": self.report_path,
        }

    def save_metadata(self):
        """写入 metadata.json，供重启后恢复"""
        meta = self.to_dict()
        meta["pytest_args"] = self.pytest_args
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / "metadata.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def from_metadata(cls, meta: dict) -> "Run":
        """从 metadata.json 恢复 Run 对象（只读，不可重新执行）"""
        run = cls.__new__(cls)
        run.run_id = meta["run_id"]
        run.module_id = meta["module_id"]
        run.pytest_args = meta.get("pytest_args", [])
        run.status = RunStatus(meta["status"])
        run.started_at = datetime.fromisoformat(meta["started_at"]) if meta.get("started_at") else None
        run.finished_at = datetime.fromisoformat(meta["finished_at"]) if meta.get("finished_at") else None
        run.exit_code = meta.get("exit_code")
        run.report_path = meta.get("report_path")
        run.run_dir = REPORTS_ROOT / run.run_id
        run.log_file = run.run_dir / "logs.txt"
        run.allure_results = run.run_dir / "allure-results"
        run.allure_report = run.run_dir / "allure-report"
        run.process = None
        run._log_queue = asyncio.Queue()
        return run


# In-memory store (single-user demo)
_runs: dict[str, Run] = {}


def get_run(run_id: str) -> Optional[Run]:
    return _runs.get(run_id)


def list_runs() -> list[Run]:
    return sorted(_runs.values(), key=lambda r: r.run_id, reverse=True)[:20]


def create_run(module_id: str, pytest_args: list[str]) -> Run:
    run = Run(module_id, pytest_args)
    _runs[run.run_id] = run
    return run


def load_history():
    """启动时从 Reports/webui-runs/ 恢复历史 run（最近20条）"""
    if not REPORTS_ROOT.exists():
        return
    dirs = sorted(REPORTS_ROOT.iterdir(), reverse=True)[:20]
    for d in dirs:
        meta_file = d / "metadata.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                run = Run.from_metadata(meta)
                # 重启后 running/queued 状态视为 failed
                if run.status in (RunStatus.running, RunStatus.queued):
                    run.status = RunStatus.failed
                _runs[run.run_id] = run
            except Exception:
                pass

