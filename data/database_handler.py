"""Database handler for CSV operations."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pandas as pd

from config import STUDENT_CSV, ATTENDANCE_DIR


def read_students() -> pd.DataFrame:
    """Read student CSV file."""
    try:
        if STUDENT_CSV.exists():
            return pd.read_csv(STUDENT_CSV)
        return pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])
    except Exception as e:
        print(f"Error reading students: {e}")
        return pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])


def append_student_row(row: dict) -> bool:
    """Append a student row to CSV."""
    try:
        # Read existing data
        if STUDENT_CSV.exists():
            df = pd.read_csv(STUDENT_CSV)
        else:
            df = pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])
        
        # Append new row
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        
        # Write back
        df.to_csv(STUDENT_CSV, index=False)
        return True
    except Exception as e:
        print(f"Error appending student: {e}")
        return False


def list_csv_files(folder: Path) -> List[str]:
    """List all CSV files in a folder."""
    try:
        if folder.exists():
            return [f.name for f in folder.glob("*.csv")]
        return []
    except Exception as e:
        print(f"Error listing CSV files: {e}")
        return []


def get_attendance_summary(csv_file: Path) -> dict:
    """Get summary of an attendance CSV file."""
    try:
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            return {
                'filename': csv_file.name,
                'record_count': len(df),
                'students': list(df['Name'].unique()) if 'Name' in df.columns else []
            }
        return {}
    except Exception as e:
        print(f"Error reading attendance summary: {e}")
        return {}


if __name__ == "__main__":
    # Test functions
    students = read_students()
    print(f"Total students: {len(students)}")
    print(students)
