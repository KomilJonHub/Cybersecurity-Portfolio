import tkinter as tk

from keyboard_monitor import AuthorizedKeyboardMonitor
from log_manager import LogManager
from ui import KeyloggerApp


def main() -> None:
    """Create the main program objects and open the interface."""

    # Create the Tkinter window.
    root = tk.Tk()

    # Create the objects used by the program.
    monitor = AuthorizedKeyboardMonitor()
    log_manager = LogManager()

    # Connect the interface to the monitor and log manager.
    KeyloggerApp(
        root,
        monitor,
        log_manager,
    )

    # Keep the window running and wait for user actions.
    root.mainloop()


# Start the program only when this file is run directly.
if __name__ == "__main__":
    main()