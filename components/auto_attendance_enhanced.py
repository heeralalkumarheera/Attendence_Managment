"""Auto attendance with personalized thank-you messages and auto-restart."""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

import cv2
import pandas as pd

from components.face_engine import FaceEngine
from config import ATTENDANCE_DIR, STUDENT_CSV
from data.database_handler import read_students
from utils.logger import log_info, log_error


def mark_auto_attendance(master: Optional[tk.Tk] = None, subject: str = "Class") -> None:
    """Auto attendance with personalized thank-you and auto-restart."""
    
    win = tk.Toplevel(master) if master else tk.Tk()
    win.title(f"Auto Attendance - {subject}")
    win.geometry("900x600")
    win.configure(bg="#0a1e3f")
    
    # Make fullscreen
    win.state('zoomed')
    
    # Title
    title_label = tk.Label(win, text=f"✅ Auto Attendance Session - {subject}", 
                          bg="#1a3a63", fg="white", font=("Arial", 28, "bold"), pady=20)
    title_label.pack(fill="x")

    status_var = tk.StringVar(value="📹 Ready... Stand in front of camera")
    status_label = tk.Label(win, textvariable=status_var, bg="#28a745", fg="white",
                            font=("Arial", 14, "bold"), pady=10, wraplength=800)
    status_label.pack(fill="x", padx=20, pady=10)

    count_var = tk.StringVar(value="Students Marked: 0")
    count_label = tk.Label(win, textvariable=count_var, bg="#0a1e3f", fg="#a8d5ff",
                           font=("Arial", 16, "bold"))
    count_label.pack(pady=10)
    
    # Message display area
    message_var = tk.StringVar(value="")
    message_label = tk.Label(win, textvariable=message_var, bg="#0a1e3f", fg="#28a745",
                            font=("Arial", 40, "bold"), pady=40)
    message_label.pack(fill="both", expand=True)
    
    # Student list
    list_frame = tk.Frame(win, bg="#0a1e3f")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    tk.Label(list_frame, text="Students Marked in this Session:", bg="#0a1e3f", fg="white",
            font=("Arial", 12, "bold")).pack(anchor="w")
    
    marked_text = tk.Text(list_frame, height=8, bg="white", font=("Arial", 11),
                         relief="sunken", bd=2)
    marked_text.pack(fill="both", expand=True)
    marked_text.config(state="disabled")

    running = [True]  # Mutable flag for controlling loop
    auto_restart_after = [2000]  # Auto-restart timer in ms

    def update_marked_list(marked_data):
        """Update the marked students list."""
        marked_text.config(state="normal")
        marked_text.delete("1.0", tk.END)
        for item in marked_data:
            marked_text.insert(tk.END, f"✓ {item['Name']} ({item['Enrollment']}) - {item['Time']}\n")
        marked_text.config(state="disabled")

    def show_thank_you(name, enrollment_id):
        """Show personalized thank-you message."""
        message_var.set(f"Thank You,\n{name}! ✨")
        status_var.set(f"✅ Attendance marked for {name} ({enrollment_id})")
        status_label.config(bg="#28a745")
        
        # Schedule message clear and auto-restart
        def restart_scan():
            message_var.set("")
            status_var.set("📹 Next student... please stand in front of camera")
            status_label.config(bg="#17a2b8")
        
        win.after(auto_restart_after[0], restart_scan)

    def run_attendance():
        status_var.set("⏳ Loading student data...")
        status_label.config(bg="#0d6efd")
        win.update()

        try:
            students_df = read_students()
            if students_df.empty:
                status_var.set("❌ No students registered!")
                status_label.config(bg="#dc3545")
                return

            enrollment_to_name = dict(zip(students_df['Enrollment'], students_df['Name']))

            engine = FaceEngine()
            if not engine.model_loaded:
                status_var.set("❌ No trained model found! Train the model first.")
                status_label.config(bg="#dc3545")
                return

            status_var.set("📹 Camera starting... Press Q to end attendance")
            status_label.config(bg="#0d6efd")
            win.update()

            cap = cv2.VideoCapture(0)
            marked_students: Set[int] = set()
            attendance_data = []
            session_start = datetime.now()
            
            # Cooldown tracking for duplicate prevention
            last_marked = {}  # enrollment_id -> timestamp

            while running[0]:
                ret, frame = cap.read()
                if not ret:
                    break

                faces = engine.detect_faces(frame)
                for x, y, w, h in faces:
                    enrollment_id, confidence = engine.recognize_face(frame, x, y, w, h)
                    
                    if confidence < 70:  # Match threshold
                        name = enrollment_to_name.get(enrollment_id, f"ID-{enrollment_id}")
                        
                        # Only mark once with cooldown period
                        current_time = datetime.now()
                        if enrollment_id not in marked_students:
                            marked_students.add(enrollment_id)
                            now = datetime.now()
                            time_str = now.strftime("%H:%M:%S")
                            attendance_data.append({
                                'Enrollment': enrollment_id,
                                'Name': name,
                                'Date': now.strftime("%Y-%m-%d"),
                                'Time': time_str
                            })
                            
                            log_info(f"Marked: {name} ({enrollment_id})")
                            count_var.set(f"Students Marked: {len(marked_students)}")
                            update_marked_list(attendance_data)
                            
                            # Show thank you message (non-blocking with auto-restart)
                            show_thank_you(name, enrollment_id)
                        
                        color = (0, 255, 0)  # Green
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)  # Red

                    engine.draw_detection(frame, x, y, w, h, f"{name} ({confidence:.1f})", color)

                cv2.imshow(f"Auto Attendance - {subject} (Press Q to end)", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    running[0] = False
                    break

            cap.release()
            cv2.destroyAllWindows()

            if attendance_data:
                now = datetime.now()
                filename = f"{subject}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                filepath = ATTENDANCE_DIR / filename
                
                df = pd.DataFrame(attendance_data)
                df.to_csv(filepath, index=False)
                
                log_info(f"Attendance saved: {filename}")
                
                status_var.set(f"✅ Attendance Complete! {len(attendance_data)} students marked.")
                status_label.config(bg="#28a745")
                message_var.set(f"Session Complete\n{len(attendance_data)} Students")
                
                # Show summary
                import time
                time.sleep(2)
                
                summary_win = tk.Toplevel(win)
                summary_win.title("Attendance Summary")
                summary_win.geometry("600x400")
                summary_win.configure(bg="#1e3a5f")
                
                tk.Label(summary_win, text=f"Attendance Summary - {subject}", 
                        bg="#2c5f8d", fg="white", font=("Arial", 16, "bold"), pady=10).pack(fill="x")
                
                summary_text = tk.Text(summary_win, font=("Arial", 11), bg="white")
                summary_text.pack(fill="both", expand=True, padx=10, pady=10)
                
                summary_text.insert(tk.END, f"Class: {subject}\n")
                summary_text.insert(tk.END, f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
                summary_text.insert(tk.END, f"Total Students: {len(attendance_data)}\n")
                summary_text.insert(tk.END, "="*50 + "\n\n")
                
                for item in attendance_data:
                    summary_text.insert(tk.END, f"{item['Name']:<25} {item['Enrollment']:<10} {item['Time']}\n")
                
                summary_text.config(state="disabled")
            else:
                status_var.set("⚠️ No attendance records created.")
                status_label.config(bg="#ffc107")

        except Exception as exc:
            log_error(f"Attendance error: {exc}")
            status_var.set(f"❌ Error: {exc}")
            status_label.config(bg="#dc3545")

    def end_session():
        """End the attendance session."""
        running[0] = False
        win.quit()

    # Buttons at bottom
    button_frame = tk.Frame(win, bg="#0a1e3f")
    button_frame.pack(fill="x", padx=20, pady=20)

    start_btn = tk.Button(button_frame, text="🎥 START ATTENDANCE", command=run_attendance,
                         bg="#28a745", fg="white", font=("Arial", 13, "bold"),
                         relief="raised", bd=3, cursor="hand2", padx=20, pady=10)
    start_btn.pack(side="left", padx=5)

    end_btn = tk.Button(button_frame, text="🚪 END SESSION", command=end_session,
                       bg="#dc3545", fg="white", font=("Arial", 13, "bold"),
                       relief="raised", bd=3, cursor="hand2", padx=20, pady=10)
    end_btn.pack(side="left", padx=5)

    info_label = tk.Label(button_frame, 
                         text="Confidence threshold: < 70 for match | Auto-thank you after 2 seconds",
                         bg="#0a1e3f", fg="#b5d3ff", font=("Arial", 10))
    info_label.pack(side="right", padx=5)

    win.mainloop()


if __name__ == "__main__":
    mark_auto_attendance(subject="Demo")
