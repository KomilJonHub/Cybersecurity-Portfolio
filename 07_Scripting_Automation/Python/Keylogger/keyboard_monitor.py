"""Visible keyboard-event capture for an authorized local lab.

The classes in this module deliberately omit stealth, persistence, networking,
credential targeting, and automatic startup.
"""

from collections.abc import Callable
from datetime import datetime
from threading import RLock
from typing import Any


EventRecord = dict[str, str]
EventCallback = Callable[[EventRecord], None]
StopCallback = Callable[[str], None]


def format_key(key: Any) -> str:
    """Convert a pynput key object into a stable, readable label."""
    character = getattr(key, "char", None)
    if character is not None:
        whitespace = {" ": "[SPACE]", "\t": "[TAB]", "\n": "[ENTER]"}
        return whitespace.get(character, character)

    name = getattr(key, "name", None)
    if name:
        return f"[{name.upper()}]"

    return f"[{key}]"


def create_pynput_listener(on_press: Callable[[Any], bool | None]) -> Any:
    """Create the external pynput listener with a friendly dependency error."""
    try:
        from pynput import keyboard
    except ImportError as error:
        raise RuntimeError(
            "The pynput package is missing. Run: "
            ".venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        ) from error
    return keyboard.Listener(on_press=on_press)


class KeyboardMonitor:
    """Capture keyboard events only while a visible session is active."""

    def __init__(
        self,
        listener_factory: Callable[[Callable[[Any], bool | None]], Any]
        | None = None,
    ) -> None:
        self.events: list[EventRecord] = []
        self.started_at: datetime | None = None
        self.stopped_at: datetime | None = None
        self.active = False
        self.stop_reason = ""
        self._listener: Any | None = None
        self._listener_factory = listener_factory or create_pynput_listener
        self._on_event: EventCallback | None = None
        self._on_stopped: StopCallback | None = None
        self._lock = RLock()

    def set_callbacks(
        self,
        on_event: EventCallback | None = None,
        on_stopped: StopCallback | None = None,
    ) -> None:
        """Attach UI callbacks after the monitor object is created."""
        self._on_event = on_event
        self._on_stopped = on_stopped

    def start(self) -> None:
        """Clear old state and start a new non-blocking listener session."""
        with self._lock:
            if self.active:
                raise RuntimeError("A monitoring session is already active.")

            self.events = []
            self.started_at = datetime.now().astimezone()
            self.stopped_at = None
            self.stop_reason = ""
            self.active = True

            try:
                self._listener = self._listener_factory(self.on_press)
                self._listener.start()
            except (OSError, RuntimeError):
                self.active = False
                self.stopped_at = datetime.now().astimezone()
                self._listener = None
                raise

    def on_press(self, key: Any) -> bool | None:
        """Store one event dictionary and stop automatically when Esc is pressed."""
        with self._lock:
            if not self.active:
                return False

            label = format_key(key)
            event = {
                "timestamp": datetime.now().astimezone().isoformat(timespec="milliseconds"),
                "key": label,
            }
            self.events.append(event)

        if self._on_event:
            self._on_event(event)

        if label == "[ESC]":
            self._finish("Esc key pressed", stop_listener=False)
            return False
        return None

    def stop(self, reason: str = "Stopped by user") -> bool:
        """Stop an active listener; return False when nothing was active."""
        return self._finish(reason, stop_listener=True)

    def _finish(self, reason: str, stop_listener: bool) -> bool:
        """Finalize session state exactly once from either UI or listener thread."""
        with self._lock:
            if not self.active:
                return False

            self.active = False
            self.stopped_at = datetime.now().astimezone()
            self.stop_reason = reason
            listener = self._listener
            self._listener = None

        if stop_listener and listener is not None:
            listener.stop()

        if self._on_stopped:
            self._on_stopped(reason)
        return True


class AuthorizedKeyboardMonitor(KeyboardMonitor):
    """KeyboardMonitor subclass that enforces explicit authorization."""

    def start(self, authorized: bool = False) -> None:
        """Start only when the visible UI authorization control is selected."""
        if not authorized:
            raise PermissionError(
                "Select the authorization checkbox before monitoring."
            )
        super().start()

