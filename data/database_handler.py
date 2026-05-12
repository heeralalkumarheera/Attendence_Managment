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
            df = pd.read_csv(STUDENT_CSV, usecols=['Enrollment', 'Name', 'Date', 'Time'], 
                            dtype={'Enrollment': str})
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            # Remove rows where Name is NaN
            df = df[df['Name'].notna()]
            return df
        return pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])
    except Exception as e:
        print(f"Error reading students: {e}")
        # Try to recover by reading all columns and filtering
        try:
            if STUDENT_CSV.exists():
                df = pd.read_csv(STUDENT_CSV)
                if 'Enrollment' in df.columns and 'Name' in df.columns:
                    df = df[['Enrollment', 'Name', 'Date', 'Time']] if 'Date' in df.columns and 'Time' in df.columns else df[['Enrollment', 'Name']]
                    df = df[df['Name'].notna()]
                    return df
        except:
            pass
        return pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])


def append_student_row(row) -> bool:
    """Append a student row to CSV."""
    try:
        # Convert list to dict if needed
        if isinstance(row, list):
            row = {'Enrollment': row[0], 'Name': row[1], 'Date': row[2], 'Time': row[3]}
        
        # Read existing data (only required columns)
        if STUDENT_CSV.exists():
            df = pd.read_csv(STUDENT_CSV, usecols=['Enrollment', 'Name', 'Date', 'Time'])
            df = df.dropna(how='all')
        else:
            df = pd.DataFrame(columns=['Enrollment', 'Name', 'Date', 'Time'])
        
        # Append new row
        new_row_df = pd.DataFrame([row])
        df = pd.concat([df, new_row_df], ignore_index=True)
        
        # Write back (only required columns)
        df[['Enrollment', 'Name', 'Date', 'Time']].to_csv(STUDENT_CSV, index=False)
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
