import os
import subprocess
import webbrowser
import ctypes
from datetime import datetime
from urllib.parse import quote_plus


def perform_action(command):

    command = command.lower().strip()

    # ========================================================
    # WEBSITES
    # ========================================================

    if "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "YouTube is open, boss."

    if "whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "WhatsApp is open, boss."

    if "gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Gmail is open, boss."

    if "google" in command and "search" not in command:
        webbrowser.open("https://www.google.com")
        return "Google is open, boss."

    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    search_phrases = [
        "search google for",
        "search google",
        "google search for",
        "search for"
    ]

    for phrase in search_phrases:

        if command.startswith(phrase):

            query = command[len(phrase):].strip()

            if query:

                webbrowser.open(
                    "https://www.google.com/search?q="
                    + quote_plus(query)
                )

                return f"Searching Google for {query}, boss."

    # ========================================================
    # NEW TAB
    # ========================================================

    if "new tab" in command:

        try:
            import pyautogui

            pyautogui.hotkey("ctrl", "t")

            return "Opening a new tab, boss."

        except Exception:

            return "I couldn't open a new tab, boss."

    # ========================================================
    # NOTEPAD
    # ========================================================

    if "notepad" in command:

        subprocess.Popen("notepad.exe")

        return "Notepad is open, boss."

    # ========================================================
    # CALCULATOR
    # ========================================================

    if "calculator" in command or command == "calc":

        subprocess.Popen("calc.exe")

        return "Calculator is open, boss."

    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if (
        "file explorer" in command
        or "open explorer" in command
        or "open files" in command
    ):

        subprocess.Popen("explorer.exe")

        return "File Explorer is open, boss."

    # ========================================================
    # DESKTOP
    # ========================================================

    if "desktop" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        os.startfile(folder)

        return "Opening your desktop, boss."

    # ========================================================
    # DOWNLOADS
    # ========================================================

    if "downloads" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(folder)

        return "Opening your downloads, boss."

    # ========================================================
    # PICTURES / PHOTOS
    # ========================================================

    if "pictures" in command or "photos" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        os.startfile(folder)

        return "Opening your pictures, boss."

    # ========================================================
    # DOCUMENTS
    # ========================================================

    if "documents" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )

        os.startfile(folder)

        return "Opening your documents, boss."

    # ========================================================
    # MUSIC
    # ========================================================

    if "music folder" in command or "open music" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Music"
        )

        os.startfile(folder)

        return "Opening your music folder, boss."

    # ========================================================
    # VIDEOS
    # ========================================================

    if "video folder" in command or "open videos" in command:

        folder = os.path.join(
            os.path.expanduser("~"),
            "Videos"
        )

        os.startfile(folder)

        return "Opening your videos, boss."

    # ========================================================
    # CHROME
    # ========================================================

    if "open chrome" in command or command == "chrome":

        chrome_paths = [

            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for path in chrome_paths:

            if os.path.exists(path):

                subprocess.Popen([path])

                return "Chrome is opening, boss."

        return "I couldn't find Chrome, boss."

    # ========================================================
    # VS CODE
    # ========================================================

    if (
        "open vs code" in command
        or "open vscode" in command
        or "visual studio code" in command
    ):

        subprocess.Popen(
            "code",
            shell=True
        )

        return "Visual Studio Code is opening, boss."

    # ========================================================
    # TASK MANAGER
    # ========================================================

    if "task manager" in command:

        subprocess.Popen("taskmgr.exe")

        return "Opening Task Manager, boss."

    # ========================================================
    # WINDOWS SETTINGS
    # ========================================================

    if "open settings" in command or command == "settings":

        os.system("start ms-settings:")

        return "Opening Windows settings, boss."

    # ========================================================
    # TIME
    # ========================================================

    if (
        "what time" in command
        or "current time" in command
        or command == "time"
    ):

        current_time = datetime.now().strftime("%I:%M %p")

        return f"It is {current_time}, boss."

    # ========================================================
    # DATE
    # ========================================================

    if (
        "what date" in command
        or "today's date" in command
        or "current date" in command
        or command == "date"
    ):

        current_date = datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return f"Today is {current_date}, boss."

    # ========================================================
    # LOCK
    # ========================================================

    if (
        "lock computer" in command
        or "lock pc" in command
        or "lock my computer" in command
    ):

        ctypes.windll.user32.LockWorkStation()

        return "Locking your computer, boss."

    # ========================================================
    # MEDIA CONTROLS
    # ========================================================

    if (
        "pause music" in command
        or "pause video" in command
        or command == "pause"
    ):

        try:

            import pyautogui

            pyautogui.press("playpause")

            return "Paused, boss."

        except Exception:

            return "I couldn't control the media, boss."

    if (
        "play music" in command
        or "resume music" in command
        or command == "play"
    ):

        try:

            import pyautogui

            pyautogui.press("playpause")

            return "Playing, boss."

        except Exception:

            return "I couldn't control the media, boss."

    if "next song" in command or "next track" in command:

        try:

            import pyautogui

            pyautogui.press("nexttrack")

            return "Moving to the next track, boss."

        except Exception:

            return "I couldn't change the track, boss."

    if "previous song" in command or "previous track" in command:

        try:

            import pyautogui

            pyautogui.press("prevtrack")

            return "Going to the previous track, boss."

        except Exception:

            return "I couldn't change the track, boss."

    # ========================================================
    # DANGEROUS COMMANDS
    # ========================================================
    # These ONLY return a request.
    # voice_ai.py will ask for confirmation.

    if (
        "shutdown computer" in command
        or "shut down computer" in command
        or "shutdown pc" in command
        or "shut down pc" in command
    ):

        return "SHUTDOWN_REQUEST"

    if (
        "restart computer" in command
        or "restart pc" in command
        or "reboot computer" in command
        or "reboot pc" in command
    ):

        return "RESTART_REQUEST"

    if (
        "sleep computer" in command
        or "put computer to sleep" in command
        or "sleep pc" in command
    ):

        return "SLEEP_REQUEST"

    # ========================================================
    # NOTHING MATCHED
    # ========================================================

    return None