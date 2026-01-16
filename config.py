from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TRAINING_DIR = BASE_DIR / "TrainingImage"
LABEL_DIR = BASE_DIR / "TrainingImageLabel"
MODEL_PATH = LABEL_DIR / "Trainner.yml"
ATTENDANCE_DIR = BASE_DIR / "Attendance"
STUDENT_CSV = BASE_DIR / "StudentDetails.csv"
CASCADE_PATH = BASE_DIR / "haarcascade_frontalface_default.xml"

# Admin credentials
ADMIN_USERNAME = "Heeralal"
ADMIN_PASSWORD = "Heera@1234"


def ensure_data_dirs() -> None:
    """Create required directories if missing."""
    for path in (TRAINING_DIR, LABEL_DIR, ATTENDANCE_DIR):
        path.mkdir(parents=True, exist_ok=True)


def ensure_student_csv() -> None:
    """Create StudentDetails.csv with header if missing or empty."""
    if not STUDENT_CSV.exists() or STUDENT_CSV.stat().st_size == 0:
        STUDENT_CSV.write_text("Enrollment,Name,Date,Time\n", encoding="utf-8")
