from datetime import datetime
from pathlib import Path

from config import LOGS_DIR
from keyboard_monitor import EventRecord


class LogManager:
    """Create and save keyboard session logs."""

    def __init__(
        self,
        logs_dir: Path = LOGS_DIR,
    ) -> None:

        self.logs_dir = Path(logs_dir)

    def ensure_logs_folder(self) -> None:
        """Create the logs folder if it does not exist."""

        self.logs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Make sure the selected path is actually a folder.
        if not self.logs_dir.is_dir():
            raise NotADirectoryError(
                f"Log location is not a folder: {self.logs_dir}"
            )

    def build_summary(
        self,
        started_at: datetime,
        stopped_at: datetime,
        event_count: int,
        stop_reason: str,
    ) -> dict[str, str]:
        """Create a dictionary containing session information."""

        duration = max(
            0.0,
            (stopped_at - started_at).total_seconds(),
        )

        # Store the session details as key-value pairs.
        return {
            "Start time": started_at.isoformat(
                timespec="seconds"
            ),
            "Stop time": stopped_at.isoformat(
                timespec="seconds"
            ),
            "Duration": f"{duration:.1f} seconds",
            "Event count": str(event_count),
            "Stop reason": stop_reason,
        }

    def build_readable_text(
        self,
        events: list[EventRecord],
    ) -> str:
        """Convert recorded events into readable text."""

        output: list[str] = []

        # These keys should not appear in the readable text section.
        ignored_keys = {
            "[SHIFT]",
            "[SHIFT_R]",
            "[CTRL]",
            "[CTRL_L]",
            "[CTRL_R]",
            "[ALT]",
            "[ALT_L]",
            "[ALT_R]",
            "[CAPS_LOCK]",
            "[ESC]",
        }

        # Process every stored key event.
        for event in events:
            key = event["key"]

            if key == "[SPACE]":
                output.append(" ")

            elif key == "[ENTER]":
                output.append("\n")

            elif key == "[TAB]":
                output.append("\t")

            elif key == "[BACKSPACE]":
                # Remove the last character if there is one.
                if output:
                    output.pop()

            elif key not in ignored_keys:
                # Add normal printable characters.
                if not (
                    key.startswith("[")
                    and key.endswith("]")
                ):
                    output.append(key)

        return "".join(output)

    def save_session(
        self,
        events: list[EventRecord],
        started_at: datetime,
        stopped_at: datetime,
        stop_reason: str,
    ) -> Path:
        """Save one session as a text file."""

        self.ensure_logs_folder()

        summary = self.build_summary(
            started_at,
            stopped_at,
            len(events),
            stop_reason,
        )

        # Create a unique file name using the date and time.
        filename = (
            f"session_"
            f"{stopped_at.strftime('%Y%m%d_%H%M%S_%f')}.txt"
        )

        output_path = self.logs_dir / filename

        # Create a new file without replacing an older session.
        with output_path.open(
            "x",
            encoding="utf-8",
            newline="\n",
        ) as log_file:

            log_file.write(
                "CIS-30A KEYBOARD LOGGER\n\n"
            )

            log_file.write(
                "SESSION INFORMATION\n"
            )

            # Write each summary item using a loop.
            for label, value in summary.items():
                log_file.write(
                    f"{label}: {value}\n"
                )

            log_file.write(
                "\nTYPED TEXT\n"
            )

            readable_text = self.build_readable_text(
                events
            )

            log_file.write(
                readable_text
                or "(No text was entered)"
            )

            log_file.write(
                "\n\nKEY EVENTS\n"
            )

            # Write the complete timeline of recorded keys.
            for event in events:
                log_file.write(
                    f"{event['timestamp']} | "
                    f"{event['key']}\n"
                )

        return output_path