"""Shared settings for the authorized keyboard-monitoring project."""

from pathlib import Path


APP_NAME = "CIS-30A Authorized Keyboard Monitor"
APP_VERSION = "1.0"
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
MAX_SESSION_SECONDS = 300  # Five-minute classroom demonstration limit.
PREVIEW_EVENT_LIMIT = 250

AUTHORIZATION_TEXT = (
    "I confirm that I own this computer or have explicit permission to test it. "
    "I will type synthetic demonstration data only."
)

DEMO_PROMPT = (
    "Synthetic typing challenge (fake data only):\n"
    "Demo user: student_demo42\n"
    "Demo passphrase: Blue-Rocket-742!\n"
    "Demo sentence: The quick blue robot counts 1, 2, 3."
)

