"""Tkinter interface for visible, authorized keyboard-monitoring sessions."""

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from config import (
    APP_NAME,
    APP_VERSION,
    AUTHORIZATION_TEXT,
    DEMO_PROMPT,
    LOGS_DIR,
    MAX_SESSION_SECONDS,
    PREVIEW_EVENT_LIMIT,
)
from keyboard_monitor import AuthorizedKeyboardMonitor, EventRecord
from log_manager import LogManager


class KeyloggerApp:
    """Create controls, validate consent, and coordinate monitor and logger objects."""

    def __init__(
        self,
        root: tk.Tk,
        monitor: AuthorizedKeyboardMonitor,
        log_manager: LogManager,
    ) -> None:
        self.root = root
        self.monitor = monitor
        self.log_manager = log_manager
        self.last_log_path: Path | None = None
        self._session_saved = True
        self._closing = False
        self._preview_lines: list[str] = []

        self.authorized_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="STOPPED - no keys are being monitored")
        self.timer_var = tk.StringVar(value="00:00 / 05:00")
        self.count_var = tk.StringVar(value="Events: 0")
        self.log_var = tk.StringVar(value=f"Log folder: {LOGS_DIR}")

        self._configure_window()
        self._build_interface()
        self.monitor.set_callbacks(self.queue_event, self.queue_stopped)
        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)

    def _configure_window(self) -> None:
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("920x760")
        self.root.minsize(780, 650)
        self.root.configure(bg="#f4f7fa")

        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
        style.configure("Start.TButton", font=("Segoe UI", 11, "bold"), padding=9)
        style.configure("Stop.TButton", font=("Segoe UI", 11, "bold"), padding=9)

    def _build_interface(self) -> None:
        container = ttk.Frame(self.root, padding=18)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            container,
            text=(
                "Visible, local-only classroom demonstration. No stealth, startup "
                "persistence, or network transmission."
            ),
            foreground="#394b59",
            wraplength=850,
        ).pack(anchor="w", pady=(3, 12))

        warning = tk.Label(
            container,
            text="IMPORTANT: Type synthetic examples only - never real passwords or private information.",
            bg="#fff4ce",
            fg="#6b4f00",
            padx=12,
            pady=9,
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        warning.pack(fill="x", pady=(0, 12))

        consent_box = ttk.LabelFrame(
            container, text="1. Authorization", padding=12, style="Section.TLabelframe"
        )
        consent_box.pack(fill="x", pady=(0, 10))
        self.consent_check = ttk.Checkbutton(
            consent_box,
            text=AUTHORIZATION_TEXT,
            variable=self.authorized_var,
        )
        self.consent_check.pack(anchor="w")

        controls = ttk.LabelFrame(
            container, text="2. Session controls", padding=12, style="Section.TLabelframe"
        )
        controls.pack(fill="x", pady=(0, 10))

        buttons = ttk.Frame(controls)
        buttons.pack(fill="x")
        self.start_button = ttk.Button(
            buttons, text="Start Monitoring", command=self.start_monitoring, style="Start.TButton"
        )
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(
            buttons,
            text="Stop Monitoring",
            command=self.stop_monitoring,
            state="disabled",
            style="Stop.TButton",
        )
        self.stop_button.pack(side="left", padx=(10, 0))
        ttk.Button(buttons, text="View Last Log", command=self.view_last_log).pack(
            side="right"
        )

        status_row = ttk.Frame(controls)
        status_row.pack(fill="x", pady=(12, 0))
        self.status_label = tk.Label(
            status_row,
            textvariable=self.status_var,
            bg="#e7f3e7",
            fg="#1b5e20",
            padx=10,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        )
        self.status_label.pack(side="left", fill="x", expand=True)
        ttk.Label(status_row, textvariable=self.timer_var, width=15, anchor="center").pack(
            side="left", padx=(10, 0)
        )
        ttk.Label(status_row, textvariable=self.count_var, width=14, anchor="e").pack(
            side="left"
        )
        ttk.Label(controls, textvariable=self.log_var, foreground="#536471").pack(
            anchor="w", pady=(8, 0)
        )

        demo = ttk.LabelFrame(
            container,
            text="3. Synthetic demonstration area",
            padding=12,
            style="Section.TLabelframe",
        )
        demo.pack(fill="both", expand=True, pady=(0, 10))
        ttk.Label(demo, text=DEMO_PROMPT, foreground="#34495e").pack(anchor="w")
        self.demo_text = scrolledtext.ScrolledText(
            demo, height=5, wrap="word", font=("Consolas", 10), undo=True
        )
        self.demo_text.pack(fill="both", expand=True, pady=(8, 0))

        preview = ttk.LabelFrame(
            container,
            text="Visible event preview",
            padding=8,
            style="Section.TLabelframe",
        )
        preview.pack(fill="both", expand=True)
        self.preview_text = scrolledtext.ScrolledText(
            preview,
            height=6,
            wrap="word",
            state="disabled",
            font=("Consolas", 9),
            background="#f8fafc",
        )
        self.preview_text.pack(fill="both", expand=True)

    def start_monitoring(self) -> None:
        """Validate consent and begin a fresh visible session."""
        if not self.authorized_var.get():
            messagebox.showwarning(
                "Authorization required",
                "Select the authorization checkbox before monitoring can begin.",
                parent=self.root,
            )
            return

        try:
            self.monitor.start(authorized=True)
        except (PermissionError, RuntimeError, OSError) as error:
            messagebox.showerror("Could not start", str(error), parent=self.root)
            return

        self._session_saved = False
        self._preview_lines = []
        self._replace_preview("")
        self.status_var.set("ACTIVE - keyboard events are visibly monitored")
        self.status_label.configure(bg="#fde7e9", fg="#9c1c1c")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.consent_check.configure(state="disabled")
        self.count_var.set("Events: 0")
        self._update_timer()
        self.demo_text.focus_set()

    def stop_monitoring(self) -> None:
        """Handle a visible Stop-button request."""
        if not self.monitor.stop("Stop button selected"):
            messagebox.showinfo(
                "No active session", "Monitoring is already stopped.", parent=self.root
            )

    def queue_event(self, event: EventRecord) -> None:
        """Move a listener-thread event safely onto Tkinter's event queue."""
        if not self._closing:
            self.root.after(0, self._show_event, event)

    def _show_event(self, event: EventRecord) -> None:
        line = f"{event['timestamp'][11:23]} {event['key']}"
        self._preview_lines.append(line)
        self._preview_lines = self._preview_lines[-PREVIEW_EVENT_LIMIT:]
        self._replace_preview("  ".join(self._preview_lines))
        self.count_var.set(f"Events: {len(self.monitor.events)}")

    def _replace_preview(self, text: str) -> None:
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", text)
        self.preview_text.see("end")
        self.preview_text.configure(state="disabled")

    def queue_stopped(self, reason: str) -> None:
        """Schedule file output after a listener or button stops the session."""
        if not self._closing:
            self.root.after(0, self._finalize_session, reason)

    def _finalize_session(self, reason: str) -> None:
        if self._session_saved:
            return
        self._session_saved = True

        try:
            if self.monitor.started_at is None or self.monitor.stopped_at is None:
                raise RuntimeError("Session times are incomplete; no log was written.")
            self.last_log_path = self.log_manager.save_session(
                self.monitor.events,
                self.monitor.started_at,
                self.monitor.stopped_at,
                reason,
            )
            self.log_var.set(f"Saved local log: {self.last_log_path}")
            self.status_var.set("STOPPED - session saved locally")
        except (OSError, ValueError, RuntimeError) as error:
            self.status_var.set("STOPPED - log could not be saved")
            messagebox.showerror("File-writing error", str(error), parent=self.root)

        self.status_label.configure(bg="#e7f3e7", fg="#1b5e20")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.consent_check.configure(state="normal")
        self.timer_var.set("00:00 / 05:00")

    def _update_timer(self) -> None:
        if not self.monitor.active or self.monitor.started_at is None:
            return

        elapsed = (datetime.now().astimezone() - self.monitor.started_at).total_seconds()
        minutes, seconds = divmod(int(elapsed), 60)
        self.timer_var.set(f"{minutes:02d}:{seconds:02d} / 05:00")

        if elapsed >= MAX_SESSION_SECONDS:
            self.monitor.stop("Five-minute session limit reached")
        else:
            self.root.after(250, self._update_timer)

    def view_last_log(self) -> None:
        if self.last_log_path is None:
            messagebox.showinfo(
                "No saved log", "Complete a session before viewing a log.", parent=self.root
            )
            return

        try:
            contents = self.log_manager.read_log(self.last_log_path)
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not read log", str(error), parent=self.root)
            return

        viewer = tk.Toplevel(self.root)
        viewer.title(f"Local log - {self.last_log_path.name}")
        viewer.geometry("760x560")
        text = scrolledtext.ScrolledText(viewer, wrap="none", font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=12, pady=12)
        text.insert("1.0", contents)
        text.configure(state="disabled")

    def handle_close(self) -> None:
        """Stop and save an active session before closing the visible window."""
        self._closing = True
        if self.monitor.active:
            self.monitor.stop("Application window closed")
            self._finalize_session("Application window closed")
        self.root.destroy()

