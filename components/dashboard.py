from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from config import ATTENDANCE_DIR
from components.analytics import compute_summary, daily_counts


class Dashboard(tk.Toplevel):
    def __init__(self, master: Optional[tk.Tk] = None):
        super().__init__(master)
        self.title("Attendance Analytics Dashboard")
        self.configure(bg="#102840")
        self.geometry("1000x700")
        self.resizable(True, True)

        self._build_header()
        self._build_summary()
        self._build_latest_files()
        self._build_daily_counts()
        self.refresh_data()

    def _build_header(self):
        header = tk.Frame(self, bg="#163a5c", height=80)
        header.pack(fill="x")
        title = tk.Label(
            header,
            text="Attendance Analytics",
            bg="#163a5c",
            fg="white",
            font=("Arial", 22, "bold"),
            pady=10,
        )
        title.pack()
        subtitle = tk.Label(
            header,
            text=f"Data source: {ATTENDANCE_DIR}",
            bg="#163a5c",
            fg="#b5d3ff",
            font=("Arial", 11),
        )
        subtitle.pack()

    def _build_summary(self):
        self.summary_frame = tk.Frame(self, bg="#102840")
        self.summary_frame.pack(fill="x", pady=10)

        self.total_files_var = tk.StringVar()
        self.total_records_var = tk.StringVar()
        self.unique_students_var = tk.StringVar()

        cards = [
            ("Total Files", self.total_files_var),
            ("Records", self.total_records_var),
            ("Unique Students", self.unique_students_var),
        ]
        for idx, (label, var) in enumerate(cards):
            card = tk.Frame(self.summary_frame, bg="#1b4670", bd=0, relief="ridge")
            card.grid(row=0, column=idx, padx=12, pady=6, sticky="nsew")
            tk.Label(card, text=label, bg="#1b4670", fg="#b5d3ff", font=("Arial", 11)).pack(pady=(10, 2))
            tk.Label(card, textvariable=var, bg="#1b4670", fg="white", font=("Arial", 18, "bold")).pack(pady=(0, 10))

        for i in range(len(cards)):
            self.summary_frame.grid_columnconfigure(i, weight=1)

    def _build_latest_files(self):
        frame = tk.LabelFrame(self, text="Latest Attendance Files", bg="#102840", fg="white")
        frame.pack(fill="both", expand=True, padx=12, pady=8)

        columns = ("file", "subject", "date", "records")
        self.latest_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.latest_tree.heading(col, text=col.title())
            self.latest_tree.column(col, width=180 if col == "file" else 120)
        self.latest_tree.pack(fill="both", expand=True, padx=8, pady=8)

        style = ttk.Style(self)
        style.configure("Treeview", background="#0f2236", fieldbackground="#0f2236", foreground="white")
        style.configure("Treeview.Heading", background="#163a5c", foreground="white")

    def _build_daily_counts(self):
        frame = tk.LabelFrame(self, text="Daily Counts", bg="#102840", fg="white")
        frame.pack(fill="both", expand=True, padx=12, pady=8)

        columns = ("date", "records")
        self.daily_tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        for col in columns:
            self.daily_tree.heading(col, text=col.title())
            self.daily_tree.column(col, width=200)
        self.daily_tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh_data(self):
        summary = compute_summary(limit=50)
        self.total_files_var.set(summary["total_files"])
        self.total_records_var.set(summary["total_records"])
        self.unique_students_var.set(summary["unique_students"])

        # Latest files
        for row in self.latest_tree.get_children():
            self.latest_tree.delete(row)
        for item in summary["latest_files"]:
            self.latest_tree.insert("", "end", values=(item["file"], item["subject"], item["date"], item["records"]))

        # Daily counts
        for row in self.daily_tree.get_children():
            self.daily_tree.delete(row)
        for date, count in daily_counts(limit=50):
            self.daily_tree.insert("", "end", values=(date, count))


def open_dashboard(master: Optional[tk.Tk] = None) -> Dashboard:
    return Dashboard(master=master)
