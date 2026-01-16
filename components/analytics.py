from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

from config import ATTENDANCE_DIR


def _parse_file_info(path: Path) -> Tuple[str, str]:
    """Parse subject and timestamp parts from filename.

    Expected format: Subject_YYYY-MM-DD_HH-MM-SS.csv
    Returns (subject, date_str)
    """
    name = path.stem
    parts = name.split("_")
    if len(parts) >= 2:
        subject = parts[0]
        date_part = "-".join(parts[1:2]) if len(parts) > 1 else ""
    else:
        subject = "unknown"
        date_part = ""
    return subject, date_part


def load_attendance_frames(limit: Optional[int] = None) -> List[pd.DataFrame]:
    """Load attendance CSVs into DataFrames (newest first)."""
    files = sorted(ATTENDANCE_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if limit:
        files = files[:limit]

    frames: List[pd.DataFrame] = []
    for fpath in files:
        try:
            df = pd.read_csv(fpath)
            df["__file__"] = fpath.name
            frames.append(df)
        except Exception:
            # Skip unreadable files
            continue
    return frames


def compute_summary(limit: Optional[int] = None) -> Dict[str, object]:
    """Compute aggregate stats across attendance CSVs."""
    files = sorted(ATTENDANCE_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if limit:
        files = files[:limit]

    total_files = len(files)
    total_records = 0
    unique_students = set()
    subject_counter: Counter[str] = Counter()
    latest_files: List[Dict[str, object]] = []

    for fpath in files:
        try:
            with open(fpath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception:
            continue

        count = len(rows)
        total_records += count
        subject, date_part = _parse_file_info(fpath)
        subject_counter[subject] += count

        for row in rows:
            enrollment = row.get("Enrollment") or row.get("ENROLLMENT")
            if enrollment:
                unique_students.add(str(enrollment))

        latest_files.append(
            {
                "file": fpath.name,
                "records": count,
                "subject": subject,
                "date": date_part,
                "path": fpath,
            }
        )

    return {
        "total_files": total_files,
        "total_records": total_records,
        "unique_students": len(unique_students),
        "per_subject": subject_counter,
        "latest_files": latest_files,
    }


def daily_counts(limit: Optional[int] = None) -> List[Tuple[str, int]]:
    """Return (date, count) tuples for attendance per day."""
    frames = load_attendance_frames(limit)
    counts: Counter[str] = Counter()
    for df in frames:
        if "Date" in df.columns:
            for d in df["Date"].dropna():
                try:
                    # normalize date format
                    dt = datetime.fromisoformat(str(d)).date()
                    counts[str(dt)] += 1
                except Exception:
                    counts[str(d)] += 1
    return sorted(counts.items(), key=lambda x: x[0], reverse=True)
