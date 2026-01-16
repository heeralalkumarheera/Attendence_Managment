from __future__ import annotations

import datetime as _dt
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def log_info(message: str) -> None:
    timestamp = _dt.datetime.now().isoformat(timespec="seconds")
    line = f"[{timestamp}] INFO: {message}\n"
    LOG_FILE.write_text(LOG_FILE.read_text(encoding="utf-8") + line if LOG_FILE.exists() else line, encoding="utf-8")


def log_error(message: str) -> None:
    timestamp = _dt.datetime.now().isoformat(timespec="seconds")
    line = f"[{timestamp}] ERROR: {message}\n"
    LOG_FILE.write_text(LOG_FILE.read_text(encoding="utf-8") + line if LOG_FILE.exists() else line, encoding="utf-8")
