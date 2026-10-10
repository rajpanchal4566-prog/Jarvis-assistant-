# ============================================================
# J.A.R.V.I.S. ACTION SYSTEM
# ============================================================

import os
import subprocess
import webbrowser
import urllib.parse
import ctypes
from datetime import datetime
from pathlib import Path

from music_player import MusicPlayer


# ============================================================
# MUSIC ENGINE
# ============================================================

music = MusicPlayer()


# ============================================================
# USER DIRECTORIES
# ============================================================

HOME = Path.home()
DESKTOP = HOME / "Desktop"
DOWNLOADS = HOME / "Downloads"
PICTURES = HOME / "Pictures"
DOCUMENTS = HOME / "Documents"


# ============================================================
# FILE SEARCH
# ============================================================

def find_file(filename):

    filename = filename.strip().strip('"').strip("'")

    if not filename:
        return None

    # Direct paths
    possible_paths = [
        Path(filename),
        DESKTOP / filename,
        DOWNLOADS / filename,
        DOCUMENTS / filename,
        PICTURES / filename,
    ]

    for path in possible_paths:

        try:

            if path.exists():
                return path

        except Exception:
            pass

    # Search common folders
    search_locations = [
        DESKTOP,
        DOWNLOADS,
        DOCUMENTS,
        PICTURES,
        HOME / "Videos",
        HOME / "Music",
    ]

    target = filename.lower()

    for location in search_locations:

        if not location.exists():
            continue

        try:

            for item in location.rglob("*"):

                try:

                    if item.name.lower() == target:
                        return item

                except Exception:
                    continue

        except Exception:
            continue

    return None


# ============================================================
# WHATSAPP NUMBER CLEANUP
# ============================================================

def clean_phone_number(number):

    number = number.strip()

    allowed = "0123456789+"

    number = "".join(
        character
        for character in number
        if character in allowed
    )

    if number.startswith("+"):
        return number[1:]

    return number


# ============================================================
# MAIN ACTION FUNCTION
# ============================================================

def perform_action(command):

    command = command.lower().strip()

    # ========================================================
    # EMPTY COMMAND
    # ========================================================

    if not command:
        return None


    # ========================================================
    # MUSIC — PLAY
    # ========================================================

    if command.startswith("play "):

        song = command[5:].strip()

        if song:

            return music.play(song)


    # ========================================================
    # MUSIC — PAUSE
    # ========================================================

    if command in [
        "pause",
        "pause music",
        "pause the music",
        "pause song",
    ]:

        return music.pause()


    # ========================================================
    # MUSIC — RESUME
    # ========================================================

    if command in [
        "resume",
        "resume music",
        "resume the music",
        "resume song",
        "continue music",
    ]:

        return music.resume()


    # ========================================================
    # MUSIC — STOP
    # ========================================================

    if command in [
        "stop music",
        "stop the music",
        "stop song",
        "stop playing",
    ]:

        return music.stop()


    # ========================================================
    # MUSIC — VOLUME UP
    # ========================================================

    if command in [
        "volume up",
        "increase volume",
        "turn volume up",
        "louder",
        "make it louder",
    ]:

        return music.volume_up()


    # ========================================================
    # MUSIC — VOLUME DOWN
    # ========================================================

    if command in [
        "volume down",
        "decrease volume",
        "turn volume down",
        "lower volume",
        "make it quieter",
    ]:

        return music.volume_down()


    # ========================================================
    # MUSIC — MUTE
    # ========================================================

    if command in [
        "mute",
        "mute music",
        "mute the music",
    ]:

        return music.mute()


    # ========================================================
    # OPEN NEW BROWSER TAB
    # ========================================================

    if (
        "open new tab" in command
        or command == "new tab"
    ):

        webbrowser.open_new_tab("about:blank")

        return "New tab opened, boss."


    # ========================================================
    # OPEN YOUTUBE
    # ========================================================

    if (
        command == "youtube"
        or command == "open youtube"
        or command == "open youtube.com"
    ):

        webbrowser.open_new_tab(
            "https://www.youtube.com"
        )

        return "YouTube is open, boss."


    # ========================================================
    # OPEN GOOGLE
    # ========================================================

    if (
        command == "google"
        or command == "open google"
    ):

        webbrowser.open_new_tab(
            "https://www.google.com"
        )

        return "Google is open, boss."


    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    if command.startswith("search google for "):

        query = command[
            len("search google for "):
        ].strip()

        if query:

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )

            webbrowser.open_new_tab(url)

            return (
                f"Searching Google for {query}, boss."
            )


    if command.startswith("google "):

        query = command[
            len("google "):
        ].strip()

        if query:

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )

            webbrowser.open_new_tab(url)

            return (
                f"Searching Google for {query}, boss."
            )


    # ========================================================
    # OPEN WHATSAPP
    # ========================================================

    if (
        command == "whatsapp"
        or command == "open whatsapp"
    ):

        webbrowser.open_new_tab(
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
            ["notepad.exe"]
        )

        return "Notepad is open, boss."


    # ========================================================
    # CALCULATOR
    # ========================================================

    if (
        command == "calculator"
        or command == "open calculator"
        or command == "open calc"
        or command == "calc"
    ):

        subprocess.Popen(
            ["calc.exe"]
        )

        return "Calculator is open, boss."


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if (
        command == "file explorer"
        or command == "open file explorer"
        or command == "open files"
        or command == "open explorer"
    ):

        subprocess.Popen(
            ["explorer.exe"]
        )

        return "File Explorer is open, boss."


    # ========================================================
    # OPEN DOWNLOADS
    # ========================================================

    if (
        command == "downloads"
        or command == "open downloads"
        or command == "open my downloads"
    ):

        os.startfile(str(DOWNLOADS))

        return "Opening Downloads, boss."


    # ========================================================
    # OPEN PICTURES
    # ========================================================

    if (
        command == "pictures"
        or command == "photos"
        or command == "open pictures"
        or command == "open photos"
    ):

        os.startfile(str(PICTURES))

        return "Opening Pictures, boss."


    # ========================================================
    # OPEN DESKTOP
    # ========================================================

    if (
        command == "desktop"
        or command == "open desktop"
    ):

        os.startfile(str(DESKTOP))

        return "Opening Desktop, boss."


    # ========================================================
    # OPEN DOCUMENTS
    # ========================================================

    if (
        command == "documents"
        or command == "open documents"
        or command == "open my documents"
    ):

        os.startfile(str(DOCUMENTS))

        return "Opening Documents, boss."


    # ========================================================
    # OPEN A FILE
    # ========================================================

    file_prefixes = [
        "open file ",
        "open the file ",
        "open ",
    ]

    for prefix in file_prefixes:

        if command.startswith(prefix):

            filename = command[len(prefix):].strip()

            # Don't treat normal applications/websites as files
            blocked_names = [
                "youtube",
                "google",
                "whatsapp",
                "calculator",
                "calc",
                "notepad",
                "file explorer",
                "downloads",
                "pictures",
                "photos",
                "desktop",
                "documents",
                "new tab",
            ]

            if filename in blocked_names:
                break

            found = find_file(filename)

            if found:

                try:

                    os.startfile(str(found))

                    return (
                        f"Opening {found.name}, boss."
                    )

                except Exception as error:

                    print(
                        "FILE OPEN ERROR:",
                        error
                    )

                    return (
                        f"I found {found.name}, "
                        "but Windows could not open it, boss."
                    )

            return (
                f"I couldn't find {filename}, boss."
            )


    # ========================================================
    # OPEN FOLDER BY NAME
    # ========================================================

    if command.startswith("open folder "):

        folder_name = command[
            len("open folder "):
        ].strip()

        folder_locations = [
            DESKTOP,
            DOWNLOADS,
            DOCUMENTS,
            PICTURES,
            HOME,
        ]

        for location in folder_locations:

            try:

                for folder in location.iterdir():

                    if (
                        folder.is_dir()
                        and folder.name.lower()
                        == folder_name
                    ):

                        os.startfile(str(folder))

                        return (
                            f"Opening {folder.name}, boss."
                        )

            except Exception:
                continue

        return (
            f"I couldn't find the folder "
            f"{folder_name}, boss."
        )


    # ========================================================
    # WHATSAPP MESSAGE
    #
    # Example:
    # "message 919876543210 hello boss"
    #
    # This opens the chat with the message filled in.
    # It does NOT automatically send it.
    # ========================================================

    if command.startswith("message "):

        remaining = command[
            len("message "):
        ].strip()

        parts = remaining.split(maxsplit=1)

        if len(parts) < 2:

            return (
                "Tell me the phone number and message, boss."
            )

        number = clean_phone_number(
            parts[0]
        )

        message = parts[1].strip()

        if len(number) < 10:

            return (
                "That doesn't look like a valid phone number, boss."
            )

        url = (
            "https://wa.me/"
            + number
            + "?text="
            + urllib.parse.quote(message)
        )

        webbrowser.open_new_tab(url)

        return (
            "I've opened WhatsApp with the message ready. "
            "You can review it and send it, boss."
        )


    # ========================================================
    # WHATSAPP MESSAGE — ALTERNATIVE PHRASE
    #
    # "send message to 919876543210 hello"
    # ========================================================

    if command.startswith("send message to "):

        remaining = command[
            len("send message to "):
        ].strip()

        parts = remaining.split(maxsplit=1)

        if len(parts) < 2:

            return (
                "Tell me the phone number and message, boss."
            )

        number = clean_phone_number(
            parts[0]
        )

        message = parts[1].strip()

        if len(number) < 10:

            return (
                "That doesn't look like a valid phone number, boss."
            )

        url = (
            "https://wa.me/"
            + number
            + "?text="
            + urllib.parse.quote(message)
        )

        webbrowser.open_new_tab(url)

        return (
            "WhatsApp is ready with your message, boss."
        )


       # ========================================================
    # TIME
    # ========================================================

    if (
        command == "time"
        or "what time is it" in command
        or "what is the time" in command
        or "tell me the time" in command
        or "current time" in command
        or "current time is" in command
        or "tell me current time" in command
    ):

        current = datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is {current}, boss."
        )


    # ========================================================
    # DATE
    # ========================================================

    if (
        command == "date"
        or "what is today's date" in command
        or "what is today date" in command
        or "what is the date" in command
        or "what date is it" in command
        or "today's date" in command
        or "todays date" in command
        or "tell me the date" in command
        or "current date" in command
        or "what date" in command
    ):

        current = datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return (
            f"Today is {current}, boss."
        )


    # ========================================================
    # DAY
    # ========================================================

    if (
        command == "day"
        or "what day is it" in command
        or "what day today" in command
        or "what day is today" in command
        or "tell me the day" in command
    ):

        current = datetime.now().strftime(
            "%A"
        )

        return (
            f"Today is {current}, boss."
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
    # OPEN SETTINGS
    # ========================================================

    if (
        command == "settings"
        or command == "open settings"
    ):

        subprocess.Popen(
            ["start", "ms-settings:"],
            shell=True
        )

        return "Opening Windows Settings, boss."


    # ========================================================
    # OPEN TASK MANAGER
    # ========================================================

    if (
        "task manager" in command
    ):

        subprocess.Popen(
            ["taskmgr.exe"]
        )

        return "Task Manager is open, boss."


    # ========================================================
    # OPEN COMMAND PROMPT
    # ========================================================

    if (
        command == "command prompt"
        or command == "open command prompt"
        or command == "open cmd"
    ):

        subprocess.Popen(
            ["cmd.exe"]
        )

        return "Command Prompt is open, boss."


    # ========================================================
    # OPEN POWERSHELL
    # ========================================================

    if (
        command == "powershell"
        or command == "open powershell"
    ):

        subprocess.Popen(
            ["powershell.exe"]
        )

        return "PowerShell is open, boss."


    # ========================================================
    # OPEN CAMERA
    # ========================================================

    if (
        command == "camera"
        or command == "open camera"
    ):

        subprocess.Popen(
            [
                "explorer.exe",
                "shell:Appsfolder"
            ]
        )

        return (
            "I opened your applications folder, boss."
        )


    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    return None