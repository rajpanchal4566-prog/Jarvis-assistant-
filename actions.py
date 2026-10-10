
import webbrowser
import subprocess
import os
import ctypes
import urllib.parse
import threading
import time
from datetime import datetime


def perform_action(command):

    command = command.lower().strip()

    # ========================================================
    # PLAY MUSIC / SONG
    # ========================================================

    if command.startswith("play "):

        song = command[5:].strip()

        if song:

            import yt_dlp
            import pyautogui

            try:

                print(f"MUSIC: Searching for {song}...")

                options = {
                    "quiet": True,
                    "extract_flat": True,
                    "noplaylist": True
                }

                with yt_dlp.YoutubeDL(options) as ydl:

                    result = ydl.extract_info(
                        "ytsearch1:" + song,
                        download=False
                    )

                entries = result.get("entries", [])

                if not entries:
                    return f"I couldn't find {song}, boss."

                video_id = entries[0].get("id")

                if not video_id:
                    return f"I couldn't find {song}, boss."

                print(
                    "MUSIC: Found video:",
                    video_id
                )

                video_url = (
                    "https://www.youtube.com/watch?v="
                    + video_id
                    + "&autoplay=1"
                )

                # Open YouTube video
                webbrowser.open_new_tab(video_url)

                # Give browser time to load
                def start_video():

                    time.sleep(5)

                    try:

                        # Bring browser forward
                        pyautogui.hotkey(
                            "alt",
                            "tab"
                        )

                        time.sleep(1)

                        # Click video area
                        screen_width, screen_height = (
                            pyautogui.size()
                        )

                        pyautogui.click(
                            screen_width // 2,
                            int(screen_height * 0.42)
                        )

                        time.sleep(1)

                        # YouTube play/pause
                        pyautogui.press("k")

                    except Exception as error:

                        print(
                            "PLAYBACK ERROR:",
                            error
                        )

                threading.Thread(
                    target=start_video,
                    daemon=True
                ).start()

                return (
                    f"Playing {song}, boss."
                )

            except Exception as error:

                print(
                    "MUSIC ERROR:",
                    error
                )

                return (
                    "I couldn't start the music, boss."
                )


    # ========================================================
    # YOUTUBE
    # ========================================================

    if (
        command == "youtube"
        or command == "open youtube"
    ):

        webbrowser.open_new_tab(
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

        webbrowser.open_new_tab(
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

        webbrowser.open_new_tab(
            "https://web.whatsapp.com"
        )

        return "WhatsApp is open, boss."


    # ========================================================
    # OPEN NEW TAB
    # ========================================================

    if (
        command == "open new tab"
        or command == "new tab"
    ):

        webbrowser.open_new_tab(
            "about:blank"
        )

        return "New tab opened, boss."


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

            webbrowser.open_new_tab(url)

            return (
                f"Searching Google for {query}, boss."
            )


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
        or command == "calc"
        or command == "open calculator"
        or command == "open calc"
    ):

        subprocess.Popen(
            ["calc.exe"]
        )

        return "Calculator is open, boss."


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if (
        command == "explorer"
        or command == "open explorer"
        or command == "open file explorer"
        or command == "open files"
    ):

        subprocess.Popen(
            ["explorer.exe"]
        )

        return "File Explorer is open, boss."


    # ========================================================
    # DOWNLOADS
    # ========================================================

    if (
        command == "downloads"
        or command == "open downloads"
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        if os.path.exists(path):

            os.startfile(path)

            return (
                "Opening Downloads, boss."
            )

        return (
            "I couldn't find your Downloads folder, boss."
        )


    # ========================================================
    # PICTURES
    # ========================================================

    if (
        command == "pictures"
        or command == "photos"
        or command == "open pictures"
        or command == "open photos"
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        if os.path.exists(path):

            os.startfile(path)

            return (
                "Opening Pictures, boss."
            )

        return (
            "I couldn't find your Pictures folder, boss."
        )


    # ========================================================
    # DESKTOP
    # ========================================================

    if (
        command == "desktop"
        or command == "open desktop"
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        if os.path.exists(path):

            os.startfile(path)

            return (
                "Opening Desktop, boss."
            )

        return (
            "I couldn't find your Desktop folder, boss."
        )


    # ========================================================
    # VIDEOS
    # ========================================================

    if (
        command == "videos"
        or command == "open videos"
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Videos"
        )

        if os.path.exists(path):

            os.startfile(path)

            return (
                "Opening Videos, boss."
            )

        return (
            "I couldn't find your Videos folder, boss."
        )


    # ========================================================
    # MUSIC FOLDER
    # ========================================================

    if (
        command == "music folder"
        or command == "open music folder"
    ):

        path = os.path.join(
            os.path.expanduser("~"),
            "Music"
        )

        if os.path.exists(path):

            os.startfile(path)

            return (
                "Opening your Music folder, boss."
            )

        return (
            "I couldn't find your Music folder, boss."
        )


    # ========================================================
    # CHROME
    # ========================================================

    if (
        command == "open chrome"
        or command == "launch chrome"
    ):

        chrome_paths = [

            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for path in chrome_paths:

            if os.path.exists(path):

                subprocess.Popen(
                    [path]
                )

                return (
                    "Chrome is open, boss."
                )

        return (
            "I couldn't find Chrome, boss."
        )


    # ========================================================
    # EDGE
    # ========================================================

    if (
        command == "open edge"
        or command == "launch edge"
    ):

        subprocess.Popen(
            ["msedge.exe"]
        )

        return (
            "Microsoft Edge is open, boss."
        )


    # ========================================================
    # TIME
    # ========================================================

    if (
        command == "time"
        or "what time is it" in command
        or "tell me the time" in command
        or "current time" in command
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
        or "what date is it" in command
        or "today's date" in command
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

        return (
            "Locking your computer, boss."
        )


    # ========================================================
    # NOTHING FOUND
    # ========================================================

    return None

