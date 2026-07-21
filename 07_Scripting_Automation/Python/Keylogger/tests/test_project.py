"""Safe unit tests; no test starts a real global keyboard listener."""

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from keyboard_monitor import AuthorizedKeyboardMonitor, KeyboardMonitor, format_key
from log_manager import LogManager
from main import validate_authorization


class FakeKey:
    def __init__(self, char=None, name=None):
        self.char = char
        self.name = name

    def __str__(self):
        return "unknown"


class FakeListener:
    def __init__(self, callback):
        self.callback = callback
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


def fake_listener_factory(callback):
    return FakeListener(callback)


class KeyboardMonitorTests(unittest.TestCase):
    def test_authorization_boolean(self):
        self.assertTrue(validate_authorization(True))
        self.assertFalse(validate_authorization(False))

    def test_printable_and_special_key_formatting(self):
        self.assertEqual(format_key(FakeKey(char="A")), "A")
        self.assertEqual(format_key(FakeKey(name="space")), "[SPACE]")
        self.assertEqual(format_key(FakeKey(name="enter")), "[ENTER]")

    def test_subclass_rejects_unauthorized_start(self):
        monitor = AuthorizedKeyboardMonitor(fake_listener_factory)
        with self.assertRaises(PermissionError):
            monitor.start(authorized=False)
        self.assertFalse(monitor.active)

    def test_session_stores_event_dictionaries_and_stops(self):
        monitor = AuthorizedKeyboardMonitor(fake_listener_factory)
        monitor.start(authorized=True)
        monitor.on_press(FakeKey(char="x"))
        self.assertEqual(monitor.events[0]["key"], "x")
        self.assertTrue(monitor.stop())
        self.assertFalse(monitor.active)
        self.assertIsNotNone(monitor.stopped_at)

    def test_escape_stops_session(self):
        reasons = []
        monitor = KeyboardMonitor(fake_listener_factory)
        monitor.set_callbacks(on_stopped=reasons.append)
        monitor.start()
        result = monitor.on_press(FakeKey(name="esc"))
        self.assertFalse(result)
        self.assertFalse(monitor.active)
        self.assertEqual(reasons, ["Esc key pressed"])

    def test_start_while_active_is_rejected(self):
        monitor = KeyboardMonitor(fake_listener_factory)
        monitor.start()
        with self.assertRaises(RuntimeError):
            monitor.start()

    def test_stop_when_inactive_returns_false(self):
        monitor = KeyboardMonitor(fake_listener_factory)
        self.assertFalse(monitor.stop())

    def test_second_session_does_not_keep_first_session_data(self):
        monitor = KeyboardMonitor(fake_listener_factory)
        monitor.start()
        monitor.on_press(FakeKey(char="a"))
        monitor.stop()
        monitor.start()
        self.assertEqual(monitor.events, [])


class LogManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = LogManager(Path(self.temp_dir.name) / "logs")
        self.start = datetime(2026, 7, 13, 12, 0, tzinfo=timezone.utc)
        self.stop = self.start + timedelta(seconds=2.5)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_readable_text_handles_space_enter_and_backspace(self):
        events = [
            {"timestamp": "t", "key": "H"},
            {"timestamp": "t", "key": "i"},
            {"timestamp": "t", "key": "[BACKSPACE]"},
            {"timestamp": "t", "key": "!"},
            {"timestamp": "t", "key": "[SPACE]"},
            {"timestamp": "t", "key": "2"},
        ]
        self.assertEqual(self.manager.build_readable_text(events), "H! 2")

    def test_save_session_creates_readable_local_file(self):
        events = [{"timestamp": "2026-07-13T12:00:00+00:00", "key": "A"}]
        path = self.manager.save_session(
            events, self.start, self.stop, "Unit test"
        )
        contents = path.read_text(encoding="utf-8")
        self.assertIn("Duration: 2.5 seconds", contents)
        self.assertIn("Event count: 1", contents)
        self.assertIn("READABLE CAPTURE\nA", contents)

    def test_log_viewer_rejects_outside_file(self):
        outside = Path(self.temp_dir.name) / "outside.txt"
        outside.write_text("not a log", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.manager.read_log(outside)

    def test_logs_path_that_is_a_file_is_rejected(self):
        invalid_path = Path(self.temp_dir.name) / "not_a_folder"
        invalid_path.write_text("file", encoding="utf-8")
        manager = LogManager(invalid_path)
        with self.assertRaises(FileExistsError):
            manager.ensure_logs_folder()


if __name__ == "__main__":
    unittest.main()
