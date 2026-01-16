"""Student registration: capture face images for training."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Optional

import cv2

from components.face_engine import FaceEngine
from config import TRAINING_DIR
from data.database_handler import append_student_row
from utils.logger import log_info, log_error
import datetime
import time


def register_student(master: Optional[tk.Tk] = None) -> None:
    """GUI to register a student by capturing face images."""
    
    win = tk.Toplevel(master) if master else tk.Tk()
    win.title("Student Registration - Capture Images")
    win.geometry("500x350")
    win.configure(bg="#1e3a5f")

    # Title
    tk.Label(win, text="📸 Student Registration", bg="#2c5f8d", fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    # Enrollment
    tk.Label(win, text="Enrollment ID:", bg="#1e3a5f", fg="white",
             font=("Arial", 12, "bold")).pack(pady=(20, 5))
    enrollment_var = tk.StringVar()
    enrollment_entry = tk.Entry(win, textvariable=enrollment_var, font=("Arial", 14), width=20)
    enrollment_entry.pack(pady=(0, 15))

    # Name
    tk.Label(win, text="Student Name:", bg="#1e3a5f", fg="white",
             font=("Arial", 12, "bold")).pack(pady=(0, 5))
    name_var = tk.StringVar()
    name_entry = tk.Entry(win, textvariable=name_var, font=("Arial", 14), width=20)
    name_entry.pack(pady=(0, 20))

    status_var = tk.StringVar(value="Ready to capture...")
    status_label = tk.Label(win, textvariable=status_var, bg="#28a745", fg="white",
                            font=("Arial", 11, "bold"), pady=8)
    status_label.pack(fill="x")

    def capture_images():
        enrollment = enrollment_var.get().strip()
        name = name_var.get().strip()

        if not enrollment or not name:
            status_var.set("❌ Enrollment and Name required!")
            status_label.config(bg="#dc3545")
            return

        status_var.set("🎥 Initializing camera... Press Q to stop, auto-stops at 30 images")
        status_label.config(bg="#0d6efd")
        win.update()

        engine = FaceEngine()
        cap = cv2.VideoCapture(0)
        sample_count = 0
        max_samples = 30

        try:
            while sample_count < max_samples:
                ret, frame = cap.read()
                if not ret:
                    break

                faces = engine.detect_faces(frame)
                for x, y, w, h in faces:
                    sample_count += 1
                    img_path = TRAINING_DIR / f"{name}.{enrollment}.{sample_count}.jpg"
                    engine.save_face_image(frame[y:y+h, x:x+w], img_path)
                    engine.draw_detection(frame, x, y, w, h, f"Capture: {sample_count}/30")

                cv2.imshow("Student Registration - Press Q to stop", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Save to StudentDetails.csv
            from datetime import datetime
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            append_student_row([enrollment, name, date_str, time_str])

            log_info(f"Registered student: {name} ({enrollment}) - {sample_count} images captured")
            status_var.set(f"✅ Registration complete! {sample_count} images captured.")
            status_label.config(bg="#28a745")

        except Exception as exc:
            log_error(f"Registration error: {exc}")
            status_var.set(f"❌ Error: {exc}")
            status_label.config(bg="#dc3545")

    capture_btn = tk.Button(win, text="🎬 CAPTURE IMAGES", command=capture_images,
                            bg="#17a2b8", fg="white", font=("Arial", 13, "bold"),
                            relief="raised", bd=3, cursor="hand2", padx=20, pady=8)
    capture_btn.pack(pady=15)

    win.mainloop()


if __name__ == "__main__":
    register_student()
