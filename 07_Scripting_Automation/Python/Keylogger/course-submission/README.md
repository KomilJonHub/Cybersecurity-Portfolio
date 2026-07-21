
# CIS-30A Course Submission: Keyboard Logger

This folder contains the version of my keyboard logger project that I prepared for the CIS-30A course submission. It focuses on the Python concepts and technical requirements listed in the project rubric.

The parent `Keylogger` folder contains the extended portfolio version, which includes additional testing files, screenshots, documentation, and setup tools.

## Project Purpose

The purpose of this project is to demonstrate how Python can record keyboard input, store key events, and save the results to a text file.

The program has a visible graphical interface and requires the user to confirm that they have permission to use the computer before recording begins. It is intended only for classroom demonstrations, personal computers, and other authorized environments.

The program does not include:

- hidden operation
- automatic startup
- network transmission
- remote access
- credential targeting

## Main Features

- Tkinter graphical interface
- permission checkbox before recording
- Start and Stop buttons
- keyboard input recording with `pynput`
- automatic stop when the Escape key is pressed
- five-minute session limit
- recorded-key counter
- text-file log output
- unique log file for each session
- error handling for missing modules and file problems

## Course Requirements Demonstrated

This project includes:

- variables
- lists and dictionaries
- strings
- custom functions and function calls
- `for` loops
- conditional statements
- custom modules
- the external `pynput` module
- classes and objects
- inheritance and a subclass
- class methods
- built-in exceptions
- file operations and file output
- a graphical user interface

## Project Files

```text
course-submission/
│
├── main.py
├── config.py
├── keyboard_monitor.py
├── log_manager.py
├── ui.py
├── requirements.txt
├── README.md
└── logs/
```

### `main.py`

Starts the program, creates the main objects, and opens the Tkinter interface.

### `config.py`

Stores the program name, file paths, session limit, and interface messages.

### `keyboard_monitor.py`

Captures keyboard events, stores them in a list, and contains the parent and child keyboard-monitor classes.

### `log_manager.py`

Processes the recorded events and writes the session information to a text file.

### `ui.py`

Creates the graphical interface and connects the buttons, keyboard monitor, and log manager.

### `requirements.txt`

Lists the external Python package required to run the program.

## How to Run the Program

### 1. Install the required package

Open Command Prompt or a terminal inside this folder and run:

```bash
pip install -r requirements.txt
```

### 2. Start the program

```bash
python main.py
```

The program can also be opened in Thonny by opening `main.py` and selecting **Run**.

## How to Test the Program

1. Open the program.
2. Click **Start** without checking the permission box.
3. Confirm that the program refuses to begin recording.
4. Check the permission box.
5. Click **Start**.
6. Type sample text in the typing area.
7. Click **Stop** or press the Escape key.
8. Open the `logs` folder.
9. Confirm that a new text file was created.

Only fake test information should be entered during the demonstration.

## Log Output

Each saved log includes:

- start time
- stop time
- session duration
- number of recorded events
- reason the session stopped
- reconstructed typed text
- complete key-event timeline

The program creates a unique filename for every session, so previous logs are not overwritten.

## Limitations

The readable text may not perfectly reproduce every keyboard action. Modifier keys, keyboard shortcuts, Caps Lock behavior, special keyboard layouts, and some key combinations may appear differently in the saved output.

The program also depends on the `pynput` package and stores the logs as regular text files.

## Future Improvements

Possible future improvements include:

- better handling of Shift and Caps Lock
- optional protection for saved log files
- user-selected log locations
- adjustable session limits
- clearer handling of keyboard shortcuts
- additional testing with different keyboard layouts

## Version Note

This is the simplified version that I prepared for my CIS-30A course submission.

The parent `Keylogger` folder contains the extended portfolio version with additional development materials and features developed leveraging more AI.
