"""Manual attendance entry."""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from typing import Optional

import pandas as pd

from config import ATTENDANCE_DIR, STUDENT_CSV
from data.database_handler import read_students
from utils.logger import log_info, log_error


def mark_manual_attendance(master: Optional[tk.Tk] = None) -> None:
    """GUI for manual attendance entry."""
    
    win = tk.Toplevel(master) if master else tk.Tk()
    win.title("Manual Attendance")
    win.geometry("700x500")
    win.configure(bg="#1e3a5f")

    tk.Label(win, text="📝 Manual Attendance Entry", bg="#2c5f8d", fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    # Subject
    tk.Label(win, text="Subject/Class Name:", bg="#1e3a5f", fg="white",
             font=("Arial", 12, "bold")).pack(pady=(20, 5))
    subject_var = tk.StringVar()
    subject_entry = tk.Entry(win, textvariable=subject_var, font=("Arial", 14), width=30)
    subject_entry.pack(pady=(0, 20))

    # Listbox for students
    tk.Label(win, text="Select Students (Ctrl+Click to select multiple):", bg="#1e3a5f", fg="white",
             font=("Arial", 12, "bold")).pack(pady=(10, 5))
    
    listbox = tk.Listbox(win, selectmode=tk.MULTIPLE, font=("Arial", 11), height=10, bg="white")
    listbox.pack(fill="both", expand=True, padx=10, pady=5)

    # Load students
    try:
        students_df = read_students()
        for _, row in students_df.iterrows():
            listbox.insert(tk.END, f"{row['Name']} ({row['Enrollment']})")
    except Exception:
        pass

    status_var = tk.StringVar(value="Ready...")
    status_label = tk.Label(win, textvariable=status_var, bg="#28a745", fg="white",
                            font=("Arial", 11, "bold"), pady=8)
    status_label.pack(fill="x")

    def save_attendance():
        subject = subject_var.get().strip()
        selections = listbox.curselection()

        if not subject:
            status_var.set("❌ Please enter subject name!")
            status_label.config(bg="#dc3545")
            return

        if not selections:
            status_var.set("❌ Please select at least one student!")
            status_label.config(bg="#dc3545")
            return

        try:
            students_df = read_students()
            attendance_data = []
            now = datetime.now()

            for idx in selections:
                item = listbox.get(idx)
                # Extract enrollment from "Name (enrollment)"
                enrollment = item.split('(')[-1].rstrip(')')
                name = item.split(' (')[0]
                attendance_data.append({
                    'Enrollment': enrollment,
                    'Name': name,
                    'Date': now.strftime("%Y-%m-%d"),
                    'Time': now.strftime("%H:%M:%S")
                })

            # Save to CSV
            filename = f"{subject}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            filepath = ATTENDANCE_DIR / filename
            
            df = pd.DataFrame(attendance_data)
            df.to_csv(filepath, index=False)

            log_info(f"Manual attendance saved: {filename} - {len(attendance_data)} students")
            status_var.set(f"✅ Attendance saved! {len(attendance_data)} students marked.")
            status_label.config(bg="#28a745")

            # Show in new window
            show_win = tk.Toplevel(win)
            show_win.title(f"Attendance Summary - {subject}")
            show_win.geometry("500x400")
            
            text_widget = tk.Text(show_win, font=("Arial", 10))
            text_widget.pack(fill="both", expand=True, padx=5, pady=5)
            text_widget.insert(tk.END, f"Attendance for {subject}\n")
            text_widget.insert(tk.END, f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            text_widget.insert(tk.END, "="*50 + "\n\n")
            
            for item in attendance_data:
                text_widget.insert(tk.END, f"{item['Name']:<20} {item['Enrollment']}\n")
            
            text_widget.config(state="disabled")

        except Exception as exc:
            log_error(f"Manual attendance error: {exc}")
            status_var.set(f"❌ Error: {exc}")
            status_label.config(bg="#dc3545")

    button_frame = tk.Frame(win, bg="#1e3a5f")
    button_frame.pack(fill="x", padx=10, pady=10)

    save_btn = tk.Button(button_frame, text="💾 SAVE ATTENDANCE", command=save_attendance,
                         bg="#28a745", fg="white", font=("Arial", 12, "bold"),
                         relief="raised", bd=3, cursor="hand2", padx=15, pady=8)
    save_btn.pack(side="left", padx=5)

    win.mainloop()


if __name__ == "__main__":
    mark_manual_attendance()
