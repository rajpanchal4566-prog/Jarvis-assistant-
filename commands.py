import os
import subprocess
import webbrowser
from pathlib import Path
import urllib.parse

from config import APPLICATIONS, WEBSITES, FOLDERS


def open_application(name):

    name = name.lower().strip()

    for app_name, app_path in APPLICATIONS.items():

        if app_name in name:

            try:

                subprocess.Popen(
                    app_path,
                    shell=True
                )

                return True

            except Exception as error:

                print("Application error:", error)

                return False

    return False


def open_website(name):

    name = name.lower().strip()

    for website_name, url in WEBSITES.items():

        if website_name in name:

            webbrowser.open(url)

            return True

    return False


def open_folder(name):

    name = name.lower().strip()

    for folder_name, folder_path in FOLDERS.items():

        if folder_name in name:

            folder_path = Path(folder_path)

            if folder_path.exists():

                os.startfile(folder_path)

                return True

    return False


def google_search(query):

    query = query.strip()

    if not query:
        return False

    encoded = urllib.parse.quote_plus(query)

    url = (
        "https://www.google.com/search?q="
        + encoded
    )

    webbrowser.open(url)

    return True


def new_tab():

    subprocess.Popen(
        "cmd /c start chrome",
        shell=True
    )

    return True


def lock_pc():

    subprocess.run(
        ["rundll32.exe", "user32.dll,LockWorkStation"],
        check=False
    )


def restart_pc():

    subprocess.Popen(
        ["shutdown", "/r", "/t", "5"]
    )


def shutdown_pc():

    subprocess.Popen(
        ["shutdown", "/s", "/t", "5"]
    )


def execute_command(command):

    command = command.lower().strip()

    # Websites

    if "open youtube" in command:

        return open_website("youtube")

    if "open google" in command:

        return open_website("google")

    if "open whatsapp web" in command:

        return open_website("whatsapp web")

    # Applications

    if "open whatsapp" in command:

        if open_application("whatsapp"):
            return True

        return open_website("whatsapp web")

    if "open chrome" in command:

        return open_application("chrome")

    if "open notepad" in command:

        return open_application("notepad")

    if "open calculator" in command:

        return open_application("calculator")

    # Folders

    for folder in FOLDERS:

        if f"open {folder}" in command:

            return open_folder(folder)

    # Google search

    if command.startswith("search google for"):

        query = command.replace(
            "search google for",
            "",
            1
        ).strip()

        return google_search(query)

    if command.startswith("google"):

        query = command.replace(
            "google",
            "",
            1
        ).strip()

        return google_search(query)

    # Browser

    if "new tab" in command:

        return new_tab()

    # Lock

    if "lock computer" in command or "lock pc" in command:

        lock_pc()

        return True

    # Restart

    if "restart computer" in command:

        restart_pc()

        return True

    # Shutdown

    if "shutdown computer" in command or "shut down computer" in command:

        shutdown_pc()

        return True

    return False