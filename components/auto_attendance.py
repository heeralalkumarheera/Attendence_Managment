"""Auto attendance marking with real-time face recognition and personalized thank-you."""
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
    """Mark attendance automatically with personalized thank-you messages."""
    
    win = tk.Toplevel(master) if master else tk.Tk()
    win.title(f"Auto Attendance - {subject}")
    win.geometry("900x600")
    win.configure(bg="#0a1e3f")
    
    # Fullscreen mode
    win.state('zoomed')
    
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
    
    # Message display area for thank-you
    message_var = tk.StringVar(value="")
    message_label = tk.Label(win, textvariable=message_var, bg="#0a1e3f", fg="#28a745",
                            font=("Arial", 40, "bold"), pady=40)
    message_label.pack(fill="both", expand=True)
    
    # Marked students list
    list_frame = tk.Frame(win, bg="#0a1e3f")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    tk.Label(list_frame, text="Students Marked in this Session:", bg="#0a1e3f", fg="white",
            font=("Arial", 12, "bold")).pack(anchor="w")
    
    marked_text = tk.Text(list_frame, height=8, bg="white", font=("Arial", 11),
                         relief="sunken", bd=2)
    marked_text.pack(fill="both", expand=True)
    marked_text.config(state="disabled")

    running = [True]
    auto_restart_timeout = [2000]  # 2 seconds in milliseconds

    def update_marked_list(marked_data):
        """Update display of marked students."""
        marked_text.config(state="normal")
        marked_text.delete("1.0", tk.END)
        for item in marked_data:
            marked_text.insert(tk.END, f"✓ {item['Name']:<20} ({item['Enrollment']:<5}) - {item['Time']}\n")
        marked_text.config(state="disabled")

    def show_thank_you(name, enrollment_id):
        """Display personalized thank-you message with auto-restart."""
        message_var.set(f"Thank You,\n{name}! ✨")
        status_var.set(f"✅ Attendance marked: {name} ({enrollment_id})")
        status_label.config(bg="#28a745")
        
        def auto_restart():
            message_var.set("")
            status_var.set("📹 Next student... stand in front of camera")
            status_label.config(bg="#17a2b8")
        
        win.after(auto_restart_timeout[0], auto_restart)

    def run_attendance():
        status_var.set("⏳ Loading student data...")
        status_label.config(bg="#0d6efd")
        win.update()

        try:
            students_df = read_students()
            if students_df.empty:
                status_var.set("❌ No students registered! Register students first.")
                status_label.config(bg="#dc3545")
                return

            enrollment_to_name = dict(zip(students_df['Enrollment'], students_df['Name']))

            engine = FaceEngine()
            if not engine.model_loaded:
                status_var.set("❌ No trained model found! Train the model first.")
                status_label.config(bg="#dc3545")
                return

            status_var.set("📹 Camera starting... Press Q to end session")
            status_label.config(bg="#0d6efd")
            win.update()

            cap = cv2.VideoCapture(0)
            marked_students: Set[int] = set()
            attendance_data = []

            thank_you_display_until = [0]  # Timestamp until which to display thank you
            
            while running[0]:
                ret, frame = cap.read()
                if not ret:
                    break

                # Check if we're in thank-you display mode
                current_time = cv2.getTickCount() / cv2.getTickFrequency()
                
                if current_time < thank_you_display_until[0]:
                    # Display thank-you message on camera feed
                    overlay = frame.copy()
                    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 180, 0), -1)
                    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
                    
                    # Get the last marked student name from attendance_data
                    if attendance_data:
                        last_name = attendance_data[-1]['Name']
                        thank_you_text = f"Thank You, {last_name}!"
                        
                        # Calculate text size and position for centering
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 2.5
                        thickness = 5
                        (text_width, text_height), _ = cv2.getTextSize(thank_you_text, font, font_scale, thickness)
                        
                        x = (frame.shape[1] - text_width) // 2
                        y = (frame.shape[0] + text_height) // 2
                        
                        # Draw text with shadow
                        cv2.putText(frame, thank_you_text, (x+3, y+3), font, font_scale, (0, 0, 0), thickness+2)
                        cv2.putText(frame, thank_you_text, (x, y), font, font_scale, (255, 255, 255), thickness)
                else:
                    # Normal face detection mode
                    faces = engine.detect_faces(frame)
                    for x, y, w, h in faces:
                        enrollment_id, confidence = engine.recognize_face(frame, x, y, w, h)
                        
                        if confidence < 70:  # Confidence threshold for match
                            name = enrollment_to_name.get(enrollment_id, f"ID-{enrollment_id}")
                            
                            if enrollment_id not in marked_students:
                                marked_students.add(enrollment_id)
                                now = datetime.now()
                                attendance_data.append({
                                    'Enrollment': enrollment_id,
                                    'Name': name,
                                    'Date': now.strftime("%Y-%m-%d"),
                                    'Time': now.strftime("%H:%M:%S")
                                })
                                
                                log_info(f"Marked: {name} ({enrollment_id})")
                                count_var.set(f"Students Marked: {len(marked_students)}")
                                update_marked_list(attendance_data)
                                win.update()
                                
                                # Show thank-you in UI
                                show_thank_you(name, enrollment_id)
                                
                                # Set timer for camera feed thank-you display (2 seconds)
                                thank_you_display_until[0] = cv2.getTickCount() / cv2.getTickFrequency() + 2.0
                            
                            color = (0, 255, 0)  # Green for recognized
                        else:
                            name = "Unknown"
                            color = (0, 0, 255)  # Red for unrecognized

                        engine.draw_detection(frame, x, y, w, h, f"{name} ({confidence:.1f})", color)

                cv2.imshow(f"Auto Attendance - {subject} (Continuous Mode - Press Q to end)", frame)
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
                status_var.set(f"✅ Session Complete! {len(attendance_data)} students marked.")
                status_label.config(bg="#28a745")
                message_var.set(f"Complete!\n{len(attendance_data)} Students")
            else:
                status_var.set("⚠️ No attendance records created.")
                status_label.config(bg="#ffc107")

        except Exception as exc:
            log_error(f"Attendance error: {exc}")
            status_var.set(f"❌ Error: {exc}")
            status_label.config(bg="#dc3545")

    def close_window():
        running[0] = False
        win.quit()

    btn_frame = tk.Frame(win, bg="#0a1e3f")
    btn_frame.pack(fill="x", padx=20, pady=20)

    tk.Button(btn_frame, text="🎥 START ATTENDANCE", command=run_attendance,
             bg="#28a745", fg="white", font=("Arial", 13, "bold"), 
             relief="raised", bd=3, cursor="hand2", padx=20, pady=10).pack(side="left", padx=5)

    tk.Button(btn_frame, text="🚪 END SESSION", command=close_window,
             bg="#dc3545", fg="white", font=("Arial", 13, "bold"),
             relief="raised", bd=3, cursor="hand2", padx=20, pady=10).pack(side="left", padx=5)
    
    info_label = tk.Label(btn_frame, 
                         text="💡 Confidence < 70 for match | Auto thank-you 2s | Press Q to end",
                         bg="#0a1e3f", fg="#b5d3ff", font=("Arial", 10))
    info_label.pack(side="right", padx=5)

    win.mainloop()


if __name__ == "__main__":
    mark_auto_attendance(subject="Demo")
