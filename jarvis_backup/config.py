from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

SECURITY_DIR = BASE_DIR / "security"
SOUNDS_DIR = BASE_DIR / "sounds"

SECURITY_DIR.mkdir(exist_ok=True)
SOUNDS_DIR.mkdir(exist_ok=True)

VOICE_PROFILE = SECURITY_DIR / "enrolled_voice.wav"

WAKE_WORDS = [
    "wake up jarvis",
    "wake up, jarvis",
    "jarvis wake up",
    "hey jarvis"
]

# Change these if your applications are installed elsewhere.
APPLICATIONS = {
    "whatsapp": os.path.expandvars(
        r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe"
    ),

    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    "notepad": "notepad.exe",

    "calculator": "calc.exe",

    "file explorer": "explorer.exe",
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "whatsapp web": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
}

FOLDERS = {
    "downloads": Path.home() / "Downloads",
    "documents": Path.home() / "Documents",
    "pictures": Path.home() / "Pictures",
    "videos": Path.home() / "Videos",
    "music": Path.home() / "Music",
    "desktop": Path.home() / "Desktop",
}