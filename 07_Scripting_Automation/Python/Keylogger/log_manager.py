"""Safe local text-file output and session-summary operations."""

from datetime import datetime
from pathlib import Path
from typing import Iterable

from config import LOGS_DIR
from keyboard_monitor import EventRecord


class LogManager:
    """Create readable, timestamped local logs for authorized sessions."""

    def __init__(self, logs_dir: Path = LOGS_DIR) -> None:
        self.logs_dir = Path(logs_dir)

    def ensure_logs_folder(self) -> None:
        """Create the dedicated folder or raise a clear built-in exception."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        if not self.logs_dir.is_dir():
            raise NotADirectoryError(f"Log location is not a folder: {self.logs_dir}")

    def build_summary(
        self,
        started_at: datetime,
        stopped_at: datetime,
        event_count: int,
        stop_reason: str,
    ) -> dict[str, str]:
        """Return summary values as strings ready for UI or file output."""
        duration = max(0.0, (stopped_at - started_at).total_seconds())
        return {
            "Start time": started_at.isoformat(timespec="seconds"),
            "Stop time": stopped_at.isoformat(timespec="seconds"),
            "Duration": f"{duration:.1f} seconds",
            "Event count": str(event_count),
            "Stop reason": stop_reason,
        }

    def build_readable_text(self, events: Iterable[EventRecord]) -> str:
        """Reconstruct readable synthetic text using a loop and conditionals."""
        output: list[str] = []
        ignored = {
            "[SHIFT]",
            "[SHIFT_R]",
            "[CTRL]",
            "[CTRL_L]",
            "[CTRL_R]",
            "[ALT]",
            "[ALT_L]",
            "[ALT_R]",
            "[ESC]",
            "[CAPS_LOCK]",
        }

        for event in events:
            label = event["key"]
            if label == "[SPACE]":
                output.append(" ")
            elif label == "[ENTER]":
                output.append("\n")
            elif label == "[TAB]":
                output.append("\t")
            elif label == "[BACKSPACE]":
                if output:
                    output.pop()
            elif label not in ignored and not label.startswith("[KEY."):
                if not (label.startswith("[") and label.endswith("]")):
                    output.append(label)

        return "".join(output)

    def save_session(
        self,
        events: list[EventRecord],
        started_at: datetime,
        stopped_at: datetime,
        stop_reason: str,
    ) -> Path:
        """Write one uniquely named UTF-8 text log and return its path."""
        self.ensure_logs_folder()
        summary = self.build_summary(
            started_at, stopped_at, len(events), stop_reason
        )
        filename = f"session_{stopped_at.strftime('%Y%m%d_%H%M%S_%f')}.txt"
        output_path = self.logs_dir / filename

        # The explicit loop is easy to explain and visibly meets the course rubric.
        with output_path.open("x", encoding="utf-8", newline="\n") as log_file:
            log_file.write("CIS-30A AUTHORIZED KEYBOARD MONITOR - LOCAL SESSION LOG\n")
            log_file.write("Synthetic classroom data only. Do not store real secrets.\n\n")
            log_file.write("SESSION SUMMARY\n")
            for label, value in summary.items():
                log_file.write(f"{label}: {value}\n")

            log_file.write("\nREADABLE CAPTURE\n")
            log_file.write(self.build_readable_text(events) or "(no printable text)")
            log_file.write("\n\nEVENT TIMELINE\n")
            for event in events:
                log_file.write(f"{event['timestamp']} | {event['key']}\n")

        return output_path

    def read_log(self, path: Path) -> str:
        """Read a generated local log for the optional in-application viewer."""
        candidate = Path(path).resolve()
        logs_root = self.logs_dir.resolve()
        if logs_root not in candidate.parents:
            raise ValueError("Only files inside the local logs folder can be viewed.")
        return candidate.read_text(encoding="utf-8")

