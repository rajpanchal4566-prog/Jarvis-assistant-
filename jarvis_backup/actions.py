def perform_action(command):
    import webbrowser
    import subprocess
    import os
    import ctypes
    from datetime import datetime

    command = command.lower().strip()

    if "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "YouTube is open, boss."

    if "google" in command:
        webbrowser.open("https://www.google.com")
        return "Google is open, boss."

    if "whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "WhatsApp is open, boss."

    if "notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Notepad is open, boss."

    if "calculator" in command or "calc" in command:
        subprocess.Popen("calc.exe")
        return "Calculator is open, boss."

    if "file explorer" in command or "open files" in command:
        subprocess.Popen("explorer.exe")
        return "File Explorer is open, boss."

    if "downloads" in command:
        os.startfile(os.path.join(os.path.expanduser("~"), "Downloads"))
        return "Opening Downloads, boss."

    if "pictures" in command or "photos" in command:
        os.startfile(os.path.join(os.path.expanduser("~"), "Pictures"))
        return "Opening Pictures, boss."

    if "desktop" in command:
        os.startfile(os.path.join(os.path.expanduser("~"), "Desktop"))
        return "Opening Desktop, boss."

    if "what time" in command or "current time" in command:
        return f"It is {datetime.now().strftime('%I:%M %p')}, boss."

    if "what date" in command or "today's date" in command:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}, boss."

    if "lock computer" in command or "lock pc" in command:
        ctypes.windll.user32.LockWorkStation()
        return "Locking your computer, boss."

    return None
