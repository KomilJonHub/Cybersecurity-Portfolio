from pathlib import Path


APP_NAME = "CIS-30A Keyboard Logger"
APP_VERSION = "1.0"

# Find the main project folder and create the logs folder path.
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"

# Stop the program automatically after five minutes.
MAX_SESSION_SECONDS = 300

# Text displayed next to the permission checkbox.
AUTHORIZATION_TEXT = "I have permission to use this computer."

# Instructions shown above the typing area.
DEMO_PROMPT = (
    "Type something in the box below to test the program.\n"
    "Do not enter real passwords or private information."
)