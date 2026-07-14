# CIS-30A Authorized Keyboard Monitor

A visible, consent-gated Python application for an authorized classroom lab.
It demonstrates how keyboard events are captured, stored in a list of event
dictionaries, displayed in a Tkinter interface, and written to a local text
file. The program is intentionally limited to five-minute synthetic-data
sessions.

## Authorized-use statement

Use this project only on a computer you own or have explicit permission to
test. Type fake demonstration data only. The application does not include
stealth, automatic startup, persistence, security-tool evasion, credential
targeting, networking, remote control, or log concealment.

## Features

- Authorization checkbox required before monitoring begins
- Visible Start and Stop buttons plus a clear ACTIVE/STOPPED indicator
- Real keyboard events captured with `pynput`
- Printable and special-key labels, including Space, Enter, Backspace, Tab,
  Shift, Ctrl, and Esc
- Esc shutdown and automatic five-minute session limit
- In-memory list of timestamped event dictionaries
- Timestamped UTF-8 text logs in the local `logs` folder
- Session start, stop, duration, event count, and stop reason
- Readable synthetic-text reconstruction plus a detailed event timeline
- In-application preview and last-log viewer
- Clear dependency, authorization, listener, path, and file-writing errors

## Architecture

```text
main.py                 Creates objects and starts the Tkinter event loop
config.py               Strings, paths, and application limits
keyboard_monitor.py     Listener class, authorization subclass, key formatting
log_manager.py          Second class, loops, summaries, and local file output
ui.py                   Consent, controls, demo area, status, timer, log viewer
tests/test_project.py   Safe tests using a fake listener
docs/                   Part 1 documents, rubric audit, and test report
logs/                   Synthetic sample; real session logs are Git-ignored
```

## Windows installation

Install a current Python 3 release from [python.org](https://www.python.org/downloads/windows/).
During installation, select **Add Python to PATH** and keep **tcl/tk and IDLE**
enabled because Tkinter needs that component.

Open PowerShell in this project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Activation is optional. If PowerShell blocks it, use the environment directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Authorized demonstration

1. Run `python main.py`.
2. Read the visible warning and select the authorization checkbox.
3. Select **Start Monitoring**; the status changes to ACTIVE.
4. Click the synthetic demonstration area and type only the fake examples shown.
5. Press **Esc** or select **Stop Monitoring**.
6. Confirm the saved local path, then select **View Last Log**.

## Tests

Run tests that use a fake listener and never monitor the real keyboard:

```powershell
python -m unittest discover -s tests -v
```

The automated suite covers authorization, printable and special keys, event
storage, Esc, duplicate starts, inactive stops, consecutive-session isolation,
readable reconstruction, file output, unsafe viewer paths, and invalid log
locations. Manual UI and keyboard-layout checks are listed in
`docs/test_report.md`.

## Sample synthetic output

```text
SESSION SUMMARY
Duration: 12.4 seconds
Event count: 18
Stop reason: Esc key pressed

READABLE CAPTURE
student_demo42
```

See `logs/sample_synthetic_log.txt` for a complete non-sensitive example.

## Course concepts demonstrated

- Variables, strings, conditionals, functions, function calls, and an explicit
  `for` loop
- A list containing event dictionaries
- External `pynput` module plus custom Python modules
- `KeyboardMonitor`, `LogManager`, and `KeyloggerApp` classes
- `AuthorizedKeyboardMonitor(KeyboardMonitor)` subclass
- Objects and methods created and called from `main.py` and `ui.py`
- Built-in exception handling and local file operations/output
- Tkinter UI for the optional bonus

## Limitations

- Keyboard layouts and operating systems can label some keys differently.
- Endpoint protection may warn about keyboard monitoring even in an authorized lab.
- Tkinter requires a Python installation that includes Tcl/Tk.
- Reconstructed text is intentionally simple and does not emulate every editor
  behavior, shortcut, cursor movement, or international input method.
- The program is not a service and is not designed for covert or remote use.
- Logs are plain text for coursework; never use them for real sensitive data.

## Defensive-security lessons

Keylogging threatens confidentiality because typed data can reveal private
messages and account secrets. Defenses include endpoint protection, least
privilege, application allow-listing, review of unfamiliar processes and
startup items, timely patching, and user awareness. Multi-factor authentication
can reduce the value of a stolen password but does not make keylogging safe.

## Future improvements

Possible safe improvements include accessibility testing, configurable local
session limits, international-keyboard tests, richer log-integrity checks, and
additional unit-test coverage. Any enhancement must preserve visible consent,
local-only operation, and synthetic testing.

