from collections.abc import Callable
from datetime import datetime
from threading import RLock
from typing import Any


# Each recorded key event will be stored as a dictionary.
EventRecord = dict[str, str]


def format_key(key: Any) -> str:
    """Convert a pressed key into a readable label."""

    # Printable characters normally have a char attribute.
    character = getattr(key, "char", None)

    if character is not None:
        special_characters = {
            " ": "[SPACE]",
            "\t": "[TAB]",
            "\n": "[ENTER]",
        }

        return special_characters.get(character, character)

    # Special keys such as Shift, Escape, and Backspace have names.
    name = getattr(key, "name", None)

    if name:
        return f"[{name.upper()}]"

    return f"[{key}]"


def create_listener(
    on_press: Callable[[Any], bool | None],
) -> Any:
    """Create the pynput keyboard listener."""

    try:
        from pynput import keyboard

    except ImportError as error:
        raise RuntimeError(
            "The pynput package is missing. "
            "Run: pip install -r requirements.txt"
        ) from error

    return keyboard.Listener(on_press=on_press)


class KeyboardMonitor:
    """Record keyboard events during an active session."""

    def __init__(self) -> None:
        # Store all recorded key events in a list.
        self.events: list[EventRecord] = []

        # Store the start and stop times of the session.
        self.started_at: datetime | None = None
        self.stopped_at: datetime | None = None

        # Track whether keyboard recording is currently active.
        self.active = False

        # These variables are used to communicate with the interface.
        self._listener: Any | None = None
        self._on_event: Callable[[EventRecord], None] | None = None
        self._on_stopped: Callable[[str], None] | None = None

        # Protect shared data because pynput runs on another thread.
        self._lock = RLock()

    def set_callbacks(
        self,
        on_event: Callable[[EventRecord], None] | None = None,
        on_stopped: Callable[[str], None] | None = None,
    ) -> None:
        """Connect the keyboard monitor to the interface."""

        self._on_event = on_event
        self._on_stopped = on_stopped

    def start(self) -> None:
        """Start a new keyboard-monitoring session."""

        with self._lock:
            # Prevent two sessions from running at the same time.
            if self.active:
                raise RuntimeError(
                    "The keyboard logger is already running."
                )

            # Clear information from the previous session.
            self.events.clear()
            self.started_at = datetime.now().astimezone()
            self.stopped_at = None
            self.active = True

            try:
                # Create and start the keyboard listener.
                self._listener = create_listener(self.on_press)
                self._listener.start()

            except (OSError, RuntimeError):
                # Reset the session if the listener cannot start.
                self.active = False
                self.stopped_at = datetime.now().astimezone()
                self._listener = None
                raise

    def on_press(self, key: Any) -> bool | None:
        """Record one key press."""

        with self._lock:
            # Ignore events if the session has already stopped.
            if not self.active:
                return False

            # Save the time and readable name of the key.
            event = {
                "timestamp": datetime.now()
                .astimezone()
                .isoformat(timespec="milliseconds"),
                "key": format_key(key),
            }

            self.events.append(event)

        # Send the new event to the interface.
        if self._on_event:
            self._on_event(event)

        # Pressing Escape stops the keyboard logger.
        if event["key"] == "[ESC]":
            self._finish(
                "Escape key pressed",
                stop_listener=False,
            )
            return False

        return None

    def stop(
        self,
        reason: str = "Stopped by user",
    ) -> bool:
        """Stop the active session."""

        return self._finish(
            reason,
            stop_listener=True,
        )

    def _finish(
        self,
        reason: str,
        stop_listener: bool,
    ) -> bool:
        """Finish the session and notify the interface."""

        with self._lock:
            # Return False if the program is already stopped.
            if not self.active:
                return False

            self.active = False
            self.stopped_at = datetime.now().astimezone()

            listener = self._listener
            self._listener = None

        # Stop the pynput listener when requested by the interface.
        if stop_listener and listener is not None:
            listener.stop()

        # Tell the interface why the session ended.
        if self._on_stopped:
            self._on_stopped(reason)

        return True


# This subclass adds a permission requirement to the parent class.
class AuthorizedKeyboardMonitor(KeyboardMonitor):
    """Require permission before keyboard recording begins."""

    def start(
        self,
        authorized: bool = False,
    ) -> None:

        if not authorized:
            raise PermissionError(
                "Confirm that you have permission before starting."
            )

        # Call the start method from the parent class.
        super().start()