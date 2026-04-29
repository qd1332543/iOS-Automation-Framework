import os
from pathlib import Path
from tools.webui.config import (
    PROJECT_ROOT, WHITELIST_PATHS, IGNORE_DIRS,
    SENSITIVE_FILES, SENSITIVE_EXTENSIONS, MAX_FILE_SIZE,
)


def _is_sensitive(rel: str) -> bool:
    p = Path(rel)
    if rel in SENSITIVE_FILES or p.name in SENSITIVE_FILES:
        return True
    if p.suffix in SENSITIVE_EXTENSIONS:
        return True
    return False


def _is_allowed(rel: str) -> bool:
    for w in WHITELIST_PATHS:
        if rel == w or rel.startswith(w + "/") or rel.startswith(w + "\\"):
            return True
    return False


def get_file_tree() -> list[dict]:
    result = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel_root = Path(root).relative_to(PROJECT_ROOT).as_posix()
        for f in sorted(files):
            rel = (rel_root + "/" + f).lstrip("./")
            if rel_root == ".":
                rel = f
            if _is_allowed(rel) and not _is_sensitive(rel):
                result.append({"path": rel, "type": "file"})
    return result


def get_file_content(rel_path: str) -> dict:
    # Prevent path traversal
    try:
        target = (PROJECT_ROOT / rel_path).resolve()
        target.relative_to(PROJECT_ROOT)
    except ValueError:
        return {"error": "Access denied"}

    if _is_sensitive(rel_path):
        return {"error": "Sensitive file, access denied"}

    if not _is_allowed(rel_path):
        return {"error": "File not in whitelist"}

    if not target.exists() or not target.is_file():
        return {"error": "File not found"}

    if target.stat().st_size > MAX_FILE_SIZE:
        return {"error": f"File exceeds 200KB limit"}

    try:
        return {"content": target.read_text(encoding="utf-8", errors="replace")}
    except Exception as e:
        return {"error": str(e)}
