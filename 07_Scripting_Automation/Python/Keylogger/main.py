"""Application entry point: create objects and launch the Tkinter UI."""

import tkinter as tk
from tkinter import messagebox

from keyboard_monitor import AuthorizedKeyboardMonitor
from log_manager import LogManager
from ui import KeyloggerApp


def validate_authorization(authorized: bool) -> bool:
    """Small testable helper used to explain Boolean validation."""
    return authorized is True


def main() -> int:
    """Create class objects and start Tkinter's event-processing loop."""
    try:
        root = tk.Tk()
        monitor = AuthorizedKeyboardMonitor()
        log_manager = LogManager()
        KeyloggerApp(root, monitor, log_manager)
        root.mainloop()
    except tk.TclError as error:
        print(f"The graphical interface could not start: {error}")
        return 1
    except Exception as error:  # Last-resort startup message for a classroom demo.
        try:
            messagebox.showerror("Application error", str(error))
        except tk.TclError:
            print(f"Application error: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

