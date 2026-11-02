"""Current regression tests, added during the portfolio refresh.

These are not the recovered historical twelve-test suite. All events are
synthetic; listeners, Tk widgets, and the GUI event loop are never started.
Run from Keylogger/: python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from keyboard_monitor import AuthorizedKeyboardMonitor, format_key
from log_manager import LogManager
from ui import KeyloggerApp


class FakeListener:
    """Only retain callbacks and lifecycle state; never access an input device."""

    def __init__(self, callback):
        self.callback = callback
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


def event(key):
    return {"timestamp": "2026-01-01T12:00:00.000+00:00", "key": key}


def setUpModule():
    # Fail closed if a future test accidentally requests the real factory.
    global listener_guard
    listener_guard = patch(
        "keyboard_monitor.create_pynput_listener",
        side_effect=AssertionError("Real keyboard listeners are forbidden in tests"),
    )
    listener_guard.start()


def tearDownModule():
    listener_guard.stop()


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.factory = Mock(side_effect=FakeListener)
        self.monitor = AuthorizedKeyboardMonitor(listener_factory=self.factory)

    def tearDown(self):
        self.monitor.stop()

    def test_authorization_rejected_before_listener_creation(self):
        with self.assertRaises(PermissionError):
            self.monitor.start()
        self.factory.assert_not_called()
        self.assertFalse(self.monitor.active)
        self.assertIsNone(self.monitor.started_at)

    def test_synthetic_event_callback_and_explicit_shutdown(self):
        seen, stopped = Mock(), Mock()
        self.monitor.set_callbacks(seen, stopped)
        self.monitor.start(authorized=True)
        listener = self.monitor._listener
        self.assertTrue(listener.started)
        self.assertIsNone(listener.callback(SimpleNamespace(char="é")))
        self.assertEqual(self.monitor.events[0]["key"], "é")
        datetime.fromisoformat(self.monitor.events[0]["timestamp"])
        seen.assert_called_once_with(self.monitor.events[0])
        self.assertTrue(self.monitor.stop("Synthetic demo finished"))
        self.assertTrue(listener.stopped)
        self.assertFalse(self.monitor.active)
        self.assertGreaterEqual(self.monitor.stopped_at, self.monitor.started_at)
        self.assertEqual(self.monitor.stop_reason, "Synthetic demo finished")
        stopped.assert_called_once_with("Synthetic demo finished")

    def test_escape_records_event_and_stops_callback(self):
        stopped = Mock()
        self.monitor.set_callbacks(on_stopped=stopped)
        self.monitor.start(authorized=True)
        listener = self.monitor._listener
        self.assertIs(listener.callback(SimpleNamespace(name="esc")), False)
        self.assertFalse(self.monitor.active)
        self.assertEqual(self.monitor.events[-1]["key"], "[ESC]")
        self.assertFalse(listener.stopped)  # Returning False ends the listener.
        self.assertFalse(self.monitor.stop())
        stopped.assert_called_once_with("Esc key pressed")

    def test_duplicate_start_does_not_replace_active_session(self):
        self.monitor.start(authorized=True)
        self.monitor.on_press(SimpleNamespace(char="x"))
        with self.assertRaises(RuntimeError):
            self.monitor.start(authorized=True)
        self.factory.assert_called_once()
        self.assertEqual([e["key"] for e in self.monitor.events], ["x"])

    def test_inactive_stop_has_no_callback(self):
        stopped = Mock()
        self.monitor.set_callbacks(on_stopped=stopped)
        self.assertFalse(self.monitor.stop())
        stopped.assert_not_called()

    def test_consecutive_sessions_isolate_event_lists(self):
        self.monitor.start(authorized=True)
        self.monitor.on_press(SimpleNamespace(char="a"))
        old_events = self.monitor.events
        self.monitor.stop()
        self.monitor.start(authorized=True)
        self.assertIsNot(self.monitor.events, old_events)
        self.assertEqual(self.monitor.events, [])
        self.assertEqual([e["key"] for e in old_events], ["a"])
        self.assertIsNone(self.monitor.stopped_at)
        self.assertEqual(self.monitor.stop_reason, "")

    def test_listener_start_failure_restores_inactive_state(self):
        failed = FakeListener(None)
        failed.start = Mock(side_effect=OSError("Synthetic device failure"))
        self.factory.side_effect = None
        self.factory.return_value = failed
        with self.assertRaisesRegex(OSError, "Synthetic device failure"):
            self.monitor.start(authorized=True)
        self.assertFalse(self.monitor.active)
        self.assertIsNone(self.monitor._listener)
        self.assertIsNotNone(self.monitor.stopped_at)

    def test_format_printable_whitespace_and_special_keys(self):
        for char, expected in [("Z", "Z"), ("é", "é"), (" ", "[SPACE]"),
                               ("\t", "[TAB]"), ("\n", "[ENTER]")]:
            with self.subTest(char=char):
                self.assertEqual(format_key(SimpleNamespace(char=char)), expected)
        self.assertEqual(format_key(SimpleNamespace(name="backspace")), "[BACKSPACE]")
        self.assertEqual(format_key("unknown"), "[unknown]")

    def test_inactive_event_is_ignored(self):
        seen = Mock()
        self.monitor.set_callbacks(on_event=seen)
        self.assertIs(self.monitor.on_press(SimpleNamespace(char="x")), False)
        self.assertEqual(self.monitor.events, [])
        seen.assert_not_called()


class LogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manager = LogManager(self.root / "logs")
        self.started = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
        self.stopped = self.started + timedelta(seconds=2, microseconds=500000)

    def save(self, events):
        return self.manager.save_session(events, self.started, self.stopped, "Synthetic stop")

    def test_readable_editing_whitespace_and_modifiers(self):
        keys = ["[BACKSPACE]", "h", "i", "[BACKSPACE]", "é", "[SPACE]",
                "[SHIFT]", "[CTRL_L]", "[F1]", "[ENTER]", "[TAB]", "x", "[ESC]"]
        self.assertEqual(self.manager.build_readable_text(map(event, keys)), "hé \n\tx")

    def test_summary_duration_and_negative_duration_clamp(self):
        summary = self.manager.build_summary(self.started, self.stopped, 3, "Synthetic stop")
        self.assertEqual(summary["Duration"], "2.5 seconds")
        self.assertEqual(summary["Event count"], "3")
        self.assertEqual(summary["Stop reason"], "Synthetic stop")
        self.assertEqual(self.manager.build_summary(
            self.stopped, self.started, 0, "test")["Duration"], "0.0 seconds")

    def test_utf8_log_roundtrip_includes_summary_and_timeline(self):
        path = self.save([event("é"), event("[ESC]")])
        contents = self.manager.read_log(path)
        self.assertEqual(contents, path.read_text(encoding="utf-8"))
        self.assertIn("Event count: 2", contents)
        self.assertIn("READABLE CAPTURE\né\n", contents)
        self.assertIn("2026-01-01T12:00:00.000+00:00 | [ESC]", contents)
        self.assertIn("Synthetic classroom data only", contents)

    def test_filename_collision_never_overwrites_existing_evidence(self):
        path = self.save([event("a")])
        original = path.read_bytes()
        with self.assertRaises(FileExistsError):
            self.save([event("b")])
        self.assertEqual(path.read_bytes(), original)

    def test_empty_capture_has_explicit_placeholder(self):
        self.assertIn("(no printable text)", self.manager.read_log(self.save([])))

    def test_viewer_rejects_parent_traversal_and_log_root(self):
        self.manager.ensure_logs_folder()
        outside = self.root / "outside.txt"
        outside.write_text("synthetic outside data", encoding="utf-8")
        for path in [outside, self.manager.logs_dir / ".." / "outside.txt",
                     self.manager.logs_dir]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.manager.read_log(path)

    def test_viewer_rejects_symlink_escape(self):
        self.manager.ensure_logs_folder()
        outside = self.root / "outside.txt"
        outside.write_text("synthetic outside data", encoding="utf-8")
        link = self.manager.logs_dir / "escape.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Symlinks unavailable: {error}")
        with self.assertRaises(ValueError):
            self.manager.read_log(link)

    def test_invalid_log_folder_does_not_replace_file(self):
        self.manager.logs_dir.write_text("keep this file", encoding="utf-8")
        with self.assertRaises(OSError):
            self.save([])
        self.assertEqual(self.manager.logs_dir.read_text(), "keep this file")


class SessionCoordinationTests(unittest.TestCase):
    """Exercise GUI coordination methods using fake objects, without a window."""

    def setUp(self):
        self.app = KeyloggerApp.__new__(KeyloggerApp)
        self.app.root = Mock()
        self.app.monitor = Mock()
        self.app.timer_var = Mock()

    def test_five_minute_limit_stops_session(self):
        self.app.monitor.active = True
        self.app.monitor.started_at = datetime.now().astimezone() - timedelta(seconds=301)
        self.app._update_timer()
        self.app.monitor.stop.assert_called_once_with("Five-minute session limit reached")
        self.app.root.after.assert_not_called()

    def test_active_timer_schedules_next_check(self):
        self.app.monitor.active = True
        self.app.monitor.started_at = datetime.now().astimezone()
        self.app._update_timer()
        self.app.monitor.stop.assert_not_called()
        self.app.root.after.assert_called_once_with(250, self.app._update_timer)

    def test_finalize_saves_once_and_restores_controls(self):
        self.app._session_saved = False
        self.app.log_manager = Mock()
        self.app.monitor.started_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.app.monitor.stopped_at = self.app.monitor.started_at + timedelta(seconds=1)
        self.app.monitor.events = [event("x")]
        for attribute in ["log_var", "status_var", "status_label", "start_button",
                          "stop_button", "consent_check"]:
            setattr(self.app, attribute, Mock())
        self.app._finalize_session("Synthetic stop")
        self.app._finalize_session("Duplicate callback")
        self.app.log_manager.save_session.assert_called_once_with(
            self.app.monitor.events, self.app.monitor.started_at,
            self.app.monitor.stopped_at, "Synthetic stop")
        self.app.start_button.configure.assert_called_once_with(state="normal")
        self.app.stop_button.configure.assert_called_once_with(state="disabled")

    def test_window_close_stops_and_finalizes_active_session(self):
        self.app.monitor.active = True
        self.app._finalize_session = Mock()
        self.app.handle_close()
        self.assertTrue(self.app._closing)
        self.app.monitor.stop.assert_called_once_with("Application window closed")
        self.app._finalize_session.assert_called_once_with("Application window closed")
        self.app.root.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
