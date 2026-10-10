
import webbrowser
import subprocess
import os
import ctypes
import urllib.parse
from datetime import datetime


def perform_action(command):

    command = command.lower().strip()

    # ========================================================
    # TIME
    # ========================================================

    if (
        command == "time"
        or "what time is it" in command
        or "tell me the time" in command
        or "current time" in command
    ):

        current = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current}, boss."


    # ========================================================
    # DATE
    # ========================================================

    if (
        command == "date"
        or "what is today's date" in command
        or "what is today date" in command
        or "what date is it" in command
        or "today's date" in command
    ):

        current = datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return f"Today is {current}, boss."


    # ========================================================
    # DAY
    # ========================================================

    if (
        command == "day"
        or "what day is it" in command
        or "what day today" in command
    ):

        current = datetime.now().strftime("%A")

        return f"Today is {current}, boss."


    # ========================================================
    # YOUTUBE
    # ========================================================

    if (
        command == "youtube"
        or command == "open youtube"
    ):

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "YouTube is open, boss."


    # ========================================================
    # GOOGLE
    # ========================================================

    if (
        command == "google"
        or command == "open google"
    ):

        webbrowser.open(
            "https://www.google.com"
        )

        return "Google is open, boss."


    # ========================================================
    # WHATSAPP
    # ========================================================

    if (
        command == "whatsapp"
        or command == "open whatsapp"
    ):

        webbrowser.open(
            "https://web.whatsapp.com"
        )

        return "WhatsApp is open, boss."


    # ========================================================
    # NOTEPAD
    # ========================================================

    if (
        command == "notepad"
        or command == "open notepad"
    ):

        subprocess.Popen(
            "notepad.exe"
        )

        return "Notepad is open, boss."


    # ========================================================
    # CALCULATOR
    # ========================================================

    if (
        command == "calculator"
        or command == "calc"
        or "open calculator" in command
    ):

        subprocess.Popen(
            "calc.exe"
        )

        return "Calculator is open, boss."


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if (
        "file explorer" in command
        or "open files" in command
        or command == "explorer"
        or command == "open explorer"
    ):

        subprocess.Popen(
            "explorer.exe"
        )

        return "File Explorer is open, boss."


    # ========================================================
    # DOWNLOADS
    # ========================================================

    if (
        "downloads" in command
        and (
            "open" in command
            or "show" in command
            or "folder" in command
        )
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(path)

        return "Opening Downloads, boss."


    # ========================================================
    # PICTURES
    # ========================================================

    if (
        "pictures" in command
        or "photos" in command
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        os.startfile(path)

        return "Opening Pictures, boss."


    # ========================================================
    # DESKTOP
    # ========================================================

    if "desktop" in command:

        path = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        os.startfile(path)

        return "Opening Desktop, boss."


    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    if command.startswith(
        "search google for "
    ):

        query = command[
            len("search google for "):
        ].strip()

        if query:

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )

            webbrowser.open(url)

            return (
                f"Searching Google for {query}, boss."
            )


    # ========================================================
    # LOCK COMPUTER
    # ========================================================

    if (
        "lock computer" in command
        or "lock pc" in command
        or command == "lock"
    ):

        ctypes.windll.user32.LockWorkStation()

        return "Locking your computer, boss."


    # ========================================================
    # UNKNOWN COMMAND
    # ========================================================

    return None

