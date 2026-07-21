import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from config import (
    APP_NAME,
    APP_VERSION,
    AUTHORIZATION_TEXT,
    DEMO_PROMPT,
    LOGS_DIR,
    MAX_SESSION_SECONDS,
)
from keyboard_monitor import (
    AuthorizedKeyboardMonitor,
    EventRecord,
)
from log_manager import LogManager


class KeyloggerApp:
    """Create and control the graphical interface."""

    def __init__(
        self,
        root: tk.Tk,
        monitor: AuthorizedKeyboardMonitor,
        log_manager: LogManager,
    ) -> None:

        # Store the objects used by the program.
        self.root = root
        self.monitor = monitor
        self.log_manager = log_manager

        # Track the timer, saving process, and closing process.
        self.auto_stop_job: str | None = None
        self.session_saved = True
        self.closing = False

        # Variables used to update text in the interface.
        self.authorized_var = tk.BooleanVar(
            value=False
        )
        self.status_var = tk.StringVar(
            value="Stopped"
        )
        self.count_var = tk.StringVar(
            value="Keys recorded: 0"
        )
        self.log_var = tk.StringVar(
            value=f"Log folder: {LOGS_DIR}"
        )

        self.configure_window()
        self.build_interface()

        # Connect keyboard events to interface methods.
        self.monitor.set_callbacks(
            self.queue_event,
            self.queue_stopped,
        )

        # Run handle_close when the user closes the window.
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.handle_close,
        )

    def configure_window(self) -> None:
        """Set the title and size of the program window."""

        self.root.title(
            f"{APP_NAME} v{APP_VERSION}"
        )
        self.root.geometry("760x520")
        self.root.minsize(650, 450)

    def build_interface(self) -> None:
        """Create the labels, buttons, and typing area."""

        container = ttk.Frame(
            self.root,
            padding=18,
        )
        container.pack(
            fill="both",
            expand=True,
        )

        # Display the program title.
        ttk.Label(
            container,
            text=APP_NAME,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            container,
            text=(
                "This program records keyboard input "
                "while it is turned on."
            ),
        ).pack(
            anchor="w",
            pady=(4, 15),
        )

        # Create the permission section.
        permission_box = ttk.LabelFrame(
            container,
            text="Permission",
            padding=12,
        )
        permission_box.pack(
            fill="x",
            pady=(0, 10),
        )

        self.authorization_check = ttk.Checkbutton(
            permission_box,
            text=AUTHORIZATION_TEXT,
            variable=self.authorized_var,
        )
        self.authorization_check.pack(
            anchor="w"
        )

        # Create the Start and Stop controls.
        controls_box = ttk.LabelFrame(
            container,
            text="Controls",
            padding=12,
        )
        controls_box.pack(
            fill="x",
            pady=(0, 10),
        )

        self.start_button = ttk.Button(
            controls_box,
            text="Start",
            command=self.start_monitoring,
        )
        self.start_button.pack(
            side="left"
        )

        self.stop_button = ttk.Button(
            controls_box,
            text="Stop",
            command=self.stop_monitoring,
            state="disabled",
        )
        self.stop_button.pack(
            side="left",
            padx=(10, 20),
        )

        # Display the recording status and number of keys.
        status_box = ttk.Frame(
            controls_box
        )
        status_box.pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Label(
            status_box,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            status_box,
            textvariable=self.count_var,
        ).pack(anchor="w")

        # Display the location of the log file.
        ttk.Label(
            container,
            textvariable=self.log_var,
            wraplength=700,
        ).pack(
            anchor="w",
            pady=(0, 10),
        )

        # Create the area where the user can type test data.
        typing_box = ttk.LabelFrame(
            container,
            text="Typing Area",
            padding=12,
        )
        typing_box.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            typing_box,
            text=DEMO_PROMPT,
            justify="left",
        ).pack(anchor="w")

        self.demo_text = scrolledtext.ScrolledText(
            typing_box,
            height=10,
            wrap="word",
            font=("Consolas", 11),
            undo=True,
        )
        self.demo_text.pack(
            fill="both",
            expand=True,
            pady=(8, 0),
        )

    def start_monitoring(self) -> None:
        """Start keyboard recording after permission is confirmed."""

        # Do not start unless the permission box is checked.
        if not self.authorized_var.get():
            messagebox.showwarning(
                "Permission required",
                "Confirm that you have permission first.",
                parent=self.root,
            )
            return

        try:
            self.monitor.start(
                authorized=True
            )

        except (
            PermissionError,
            RuntimeError,
            OSError,
        ) as error:
            messagebox.showerror(
                "Unable to start",
                str(error),
                parent=self.root,
            )
            return

        # Update the interface when recording begins.
        self.session_saved = False
        self.status_var.set("Recording...")
        self.count_var.set(
            "Keys recorded: 0"
        )
        self.log_var.set(
            f"Log folder: {LOGS_DIR}"
        )

        self.start_button.configure(
            state="disabled"
        )
        self.stop_button.configure(
            state="normal"
        )
        self.authorization_check.configure(
            state="disabled"
        )

        # Stop automatically after the allowed time.
        self.auto_stop_job = self.root.after(
            MAX_SESSION_SECONDS * 1000,
            self.stop_for_time_limit,
        )

        # Place the cursor inside the typing box.
        self.demo_text.focus_set()

    def stop_monitoring(self) -> None:
        """Stop recording when the Stop button is clicked."""

        if not self.monitor.stop(
            "Stop button clicked"
        ):
            messagebox.showinfo(
                "Already stopped",
                "The keyboard logger is not running.",
                parent=self.root,
            )

    def stop_for_time_limit(self) -> None:
        """Stop recording when five minutes have passed."""

        self.auto_stop_job = None

        if self.monitor.active:
            self.monitor.stop(
                "Five-minute limit reached"
            )

    def queue_event(
        self,
        _event: EventRecord,
    ) -> None:
        """Schedule an event-count update in Tkinter."""

        if not self.closing:
            self.root.after(
                0,
                self.update_event_count,
            )

    def update_event_count(self) -> None:
        """Display the current number of recorded keys."""

        self.count_var.set(
            f"Keys recorded: "
            f"{len(self.monitor.events)}"
        )

    def queue_stopped(
        self,
        reason: str,
    ) -> None:
        """Schedule the saving process after recording stops."""

        if not self.closing:
            self.root.after(
                0,
                self.finalize_session,
                reason,
            )

    def finalize_session(
        self,
        reason: str,
    ) -> None:
        """Save the recorded session and reset the buttons."""

        # Prevent the same session from being saved twice.
        if self.session_saved:
            return

        self.session_saved = True

        # Cancel the automatic stop timer if it is still active.
        if self.auto_stop_job is not None:
            self.root.after_cancel(
                self.auto_stop_job
            )
            self.auto_stop_job = None

        try:
            # Make sure the session has valid start and stop times.
            if (
                self.monitor.started_at is None
                or self.monitor.stopped_at is None
            ):
                raise RuntimeError(
                    "The session time is incomplete."
                )

            # Save the collected keyboard events.
            output_path = (
                self.log_manager.save_session(
                    self.monitor.events,
                    self.monitor.started_at,
                    self.monitor.stopped_at,
                    reason,
                )
            )

            self.status_var.set(
                "Stopped - log saved"
            )
            self.log_var.set(
                f"Saved file: {output_path}"
            )

        except (
            OSError,
            ValueError,
            RuntimeError,
        ) as error:
            self.status_var.set(
                "Stopped - log was not saved"
            )

            messagebox.showerror(
                "File error",
                str(error),
                parent=self.root,
            )

        # Reset the interface for another session.
        self.start_button.configure(
            state="normal"
        )
        self.stop_button.configure(
            state="disabled"
        )
        self.authorization_check.configure(
            state="normal"
        )

    def handle_close(self) -> None:
        """Save an active session before closing the window."""

        self.closing = True

        # Stop and save the current session before closing.
        if self.monitor.active:
            self.monitor.stop(
                "Program window closed"
            )
            self.finalize_session(
                "Program window closed"
            )

        self.root.destroy()