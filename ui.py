import customtkinter as ctk
import subprocess
import sys
import os
from pathlib import Path
from tkinter import messagebox
from datetime import datetime
import threading

# Appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Project paths
BASE_DIR = Path(__file__).resolve().parent
MONITORED_DIR = BASE_DIR / "monitored_files"
BASELINE_FILE = BASE_DIR / "baseline.json"
REPORT_FILE = BASE_DIR / "report.txt"
LOG_FILE = BASE_DIR / "integrity.log"


class FileIntegrityMonitor(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("File Integrity Monitor")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_dashboard()

        self.update_status()

    # ---------------- SIDEBAR ----------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="🛡 FIM Monitor",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self.sidebar,
            text="File Integrity Security",
            font=("Arial", 12)
        ).pack(pady=(0, 30))

        ctk.CTkButton(
            self.sidebar,
            text="🔍 Scan Files",
            height=42,
            command=self.scan_files
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="📂 Open Folder",
            height=42,
            command=self.open_folder
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="📄 View Report",
            height=42,
            command=self.view_report
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="📋 View Logs",
            height=42,
            command=self.view_logs
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="♻ Reset Baseline",
            height=42,
            fg_color="#b45309",
            hover_color="#92400e",
            command=self.reset_baseline
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkLabel(
            self.sidebar,
            text="Python + CustomTkinter",
            font=("Arial", 11)
        ).pack(side="bottom", pady=20)

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

        self.main = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25
        )

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(3, weight=1)

        # Heading
        ctk.CTkLabel(
            self.main,
            text="File Integrity Dashboard",
            font=("Arial", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        ctk.CTkLabel(
            self.main,
            text="Monitor file changes using SHA-256 hashing.",
            font=("Arial", 14),
            text_color="gray"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 20)
        )

        # Information cards
        cards = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        cards.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        for column in range(3):
            cards.grid_columnconfigure(column, weight=1)

        self.baseline_card = self.create_card(
            cards, 0, "BASELINE", "Not Created"
        )

        self.files_card = self.create_card(
            cards, 1, "MONITORED FILES", "0"
        )

        self.scan_card = self.create_card(
            cards, 2, "LAST SCAN", "Not Run"
        )

        # Output area
        output_frame = ctk.CTkFrame(self.main)

        output_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(25, 0)
        )

        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            output_frame,
            text="Scan Results",
            font=("Arial", 19, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=15
        )

        self.output = ctk.CTkTextbox(
            output_frame,
            font=("Consolas", 13),
            wrap="word"
        )

        self.output.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        self.output.insert(
            "end",
            "Welcome to File Integrity Monitor!\n\n"
            "1. Click Scan Files to create your first baseline.\n"
            "2. Modify a file in the monitored_files folder.\n"
            "3. Scan again to detect changes.\n\n"
            "Results will appear here."
        )

        self.output.configure(state="disabled")

        self.status_label = ctk.CTkLabel(
            self.main,
            text="Status: Ready",
            font=("Arial", 12),
            text_color="gray"
        )

        self.status_label.grid(
            row=4,
            column=0,
            sticky="w",
            pady=(12, 0)
        )

    # ---------------- CARDS ----------------

    def create_card(self, parent, column, title, value):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12),
            text_color="gray"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 17, "bold")
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        return value_label

    # ---------------- OUTPUT ----------------

    def show_output(self, text):

        self.output.configure(state="normal")

        self.output.delete("1.0", "end")

        self.output.insert("end", text)

        self.output.configure(state="disabled")

    # ---------------- STATUS ----------------

    def update_status(self):

        MONITORED_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        file_count = sum(
            1 for item in MONITORED_DIR.rglob("*")
            if item.is_file()
        )

        self.files_card.configure(
            text=str(file_count)
        )

        self.baseline_card.configure(
            text=(
                "Created"
                if BASELINE_FILE.exists()
                else "Not Created"
            )
        )

        self.scan_card.configure(
            text=(
                "Available"
                if REPORT_FILE.exists()
                else "Not Run"
            )
        )

    # ---------------- SCAN FILES ----------------

    def scan_files(self):

        self.status_label.configure(
            text="Status: Scanning files..."
        )

        self.show_output(
            "Scanning files...\nPlease wait."
        )

        threading.Thread(
            target=self.run_scan,
            daemon=True
        ).start()

    def run_scan(self):

        try:

            result = subprocess.run(
                [sys.executable, "main.py"],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                timeout=60
            )

            output = result.stdout

            if result.stderr:
                output += "\n\nMessages:\n" + result.stderr

            if result.returncode != 0:
                output = (
                    f"Scan failed with exit code "
                    f"{result.returncode}\n\n{output}"
                )

            elif not output.strip():
                output = "Scan finished. Check report.txt."

        except Exception as error:

            output = f"Error running scan:\n{error}"

        self.after(
            0,
            self.finish_scan,
            output
        )

    def finish_scan(self, output):

        self.show_output(output)

        self.status_label.configure(
            text="Status: Scan completed"
        )

        self.update_status()

        if "MODIFIED" in output:
            messagebox.showwarning(
                "File Modification Detected",
                "One or more monitored files have changed!"
            )

        elif "DELETED" in output:
            messagebox.showwarning(
                "File Deletion Detected",
                "One or more monitored files have been deleted!"
            )

        elif "NEW" in output:
            messagebox.showinfo(
                "New File Detected",
                "A new file has been detected."
            )

    # ---------------- OPEN FOLDER ----------------

    def open_folder(self):

        MONITORED_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        try:

            if sys.platform.startswith("win"):
                os.startfile(str(MONITORED_DIR))

            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["open", str(MONITORED_DIR)]
                )

            else:
                subprocess.Popen(
                    ["xdg-open", str(MONITORED_DIR)]
                )

        except Exception as error:

            messagebox.showerror(
                "Folder Error",
                str(error)
            )

    # ---------------- VIEW REPORT ----------------

    def view_report(self):

        self.display_file(
            REPORT_FILE,
            "Report"
        )

    # ---------------- VIEW LOGS ----------------

    def view_logs(self):

        self.display_file(
            LOG_FILE,
            "Integrity Logs"
        )

    def display_file(self, file_path, title):

        if not file_path.exists():

            messagebox.showinfo(
                title,
                "This file has not been created yet.\n"
                "Please run a scan first."
            )

            return

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

            self.show_output(
                f"{title}\n"
                f"{'=' * len(title)}\n\n"
                f"{content}"
            )

        except Exception as error:

            messagebox.showerror(
                "File Error",
                str(error)
            )

    # ---------------- RESET BASELINE ----------------

    def reset_baseline(self):

        if not BASELINE_FILE.exists():

            messagebox.showinfo(
                "Baseline",
                "No baseline exists yet."
            )

            return

        answer = messagebox.askyesno(
            "Reset Baseline",
            "Delete the current baseline?\n\n"
            "The next scan will create a new baseline "
            "from the current monitored files."
        )

        if answer:

            try:

                BASELINE_FILE.unlink()

                self.update_status()

                self.show_output(
                    "Baseline reset successfully.\n\n"
                    "Click Scan Files to create a new baseline."
                )

                self.status_label.configure(
                    text="Status: Baseline reset"
                )

            except Exception as error:

                messagebox.showerror(
                    "Reset Error",
                    str(error)
                )


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    MONITORED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    app = FileIntegrityMonitor()

    app.mainloop()

