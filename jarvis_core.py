
import os
import time
import subprocess
import webbrowser
import urllib.parse
import datetime
import re

import speech_recognition as sr

from ai_brain import ask_ai
from actions import perform_action
from security import verify_user


class JarvisCore:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, hud=None):

        self.hud = hud

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        # JARVIS starts asleep
        self.awake = False
   
        # JARVIS process stays alive
        self.running = True

        # True while JARVIS is speaking
        self.speaking = False

        self.speech_process = None


    # =========================================================
    # HUD
    # =========================================================

    def hud_state(self, state):

        if self.hud is None:
            return

        try:
            self.hud.set_state(state)
        except Exception:
            pass


    # =========================================================
    # SPEAK
    # =========================================================

    def speak(self, text):

        if not text:
            return

        self.speaking = True

        self.hud_state("SPEAKING")

        print()
        print("JARVIS:", text)

        safe_text = str(text).replace("'", "''")

        command = (
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$s.Speak('{safe_text}')"
        )

        try:

            self.speech_process = subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    command
                ]
            )

            self.speech_process.wait()

        except Exception as error:

            print("SPEECH ERROR:", error)

        finally:

            self.speech_process = None

            # Prevent microphone from immediately hearing JARVIS
            time.sleep(0.5)

            self.speaking = False

            if self.awake:
                self.hud_state("STANDBY")
            else:
                self.hud_state("SLEEPING")


    # =========================================================
    # LISTEN
    # =========================================================

    def listen(self, timeout=10, phrase_limit=10):

        # Never listen while speaking
        if self.speaking:
            return ""

        print("ENTERING LISTEN")
        print("RUN STATE:", self.running, self.awake, self.speaking)

        self.hud_state("LISTENING")

        try:

            with sr.Microphone() as source:

                print("\nListening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )

            self.hud_state("PROCESSING")

            print("Processing...")

            text = self.recognizer.recognize_google(
                audio
            )

            text = text.lower().strip()

            print("YOU:", text)

            return text

        except sr.WaitTimeoutError:

            self.hud_state(
                "STANDBY" if self.awake else "SLEEPING"
            )

            return ""

        except sr.UnknownValueError:

            print("I couldn't understand that.")

            self.hud_state(
                "STANDBY" if self.awake else "SLEEPING"
            )

            return ""

        except sr.RequestError:

            print(
                "Speech recognition service unavailable."
            )

            self.hud_state(
                "STANDBY" if self.awake else "SLEEPING"
            )

            return ""

        except Exception as error:

            print(
                "LISTEN ERROR:",
                error
            )

            self.hud_state(
                "STANDBY" if self.awake else "SLEEPING"
            )

            return ""


    # =========================================================
    # WAKE LISTENER
    # =========================================================

    def wait_for_wake(self):

        # Always start this function asleep
        self.awake = False
        self.hud_state("SLEEPING")

        print()
        print("=" * 60)
        print("JARVIS IS SLEEPING")
        print("Say: Wake up Jarvis")
        print("=" * 60)

        try:

            with sr.Microphone() as source:

                print("Calibrating microphone...")

                try:
                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=0.5
                    )
                except Exception:
                    pass

                print("Wake listener ready.")

                while self.running and not self.awake:

                    try:

                        audio = self.recognizer.listen(
                            source,
                            timeout=None,
                            phrase_time_limit=4
                        )

                        text = self.recognizer.recognize_google(
                            audio
                        ).lower().strip()

                        print(
                            "WAKE LISTENER:",
                            text
                        )

                        # -------------------------------------------------
                        # WAKE WORDS
                        # -------------------------------------------------

                        wake_words = [

                            "wake up jarvis",
                            "wake jarvis",
                            "hey jarvis",
                            "jarvis wake up",
                            "wakeup jarvis",

                            "listen jarvis",
                            "hello jarvis",
                            "hii jarvis",

                            "jarvis uth jao",
                            "uthja jarvis",
                            "subah ho gayi uthja jarvis",

                            "suno jarvis",
                            "how are you jarvis",
                            "i am back jarvis",
                            "helloowwww jarvis"

                        ]

                        # -------------------------------------------------
                        # WAKE WORD DETECTED
                        # -------------------------------------------------

                        if any(
                            phrase in text
                            for phrase in wake_words
                        ):

                            print()
                            print(
                                "WAKE WORD DETECTED."
                            )

                            print(
                                "Starting voice authentication..."
                            )

                            # -------------------------------------------------
                            # VOICE AUTHENTICATION
                            # -------------------------------------------------

                            try:

                                authenticated = verify_user()

                            except Exception as error:

                                print(
                                    "SECURITY ERROR:",
                                    error
                                )

                                authenticated = False

                            # -------------------------------------------------
                            # AUTHENTICATION FAILED
                            # -------------------------------------------------

                            if not authenticated:

                                self.awake = False

                                self.hud_state(
                                    "SLEEPING"
                                )

                                print(
                                    "VOICE AUTHENTICATION FAILED."
                                )

                                self.speak(
                                    "Voice authentication failed. Access denied."
                                )

                                # Remain in wake-listener mode
                                continue

                            # -------------------------------------------------
                            # AUTHENTICATION SUCCESSFUL
                            # -------------------------------------------------

                            print()
                            print(
                                "VOICE AUTHENTICATION SUCCESSFUL."
                            )

                            self.awake = True

                            self.hud_state(
                                "WAKE"
                            )

                            self.speak(
                                "Yes, boss?"
                            )

                            return

                    except sr.UnknownValueError:

                        # Couldn't understand the audio.
                        # Stay asleep and continue listening.

                        continue

                    except sr.RequestError:

                        print(
                            "Wake-word recognition unavailable."
                        )

                        time.sleep(2)

                    except Exception as error:

                        print(
                            "WAKE ERROR:",
                            error
                        )

                        time.sleep(1)

        except Exception as error:

            print(
                "MICROPHONE ERROR:",
                error
            )

            time.sleep(2)


    # =========================================================
    # SLEEP
    # =========================================================

    def sleep(self):

        # IMPORTANT:
        # Set awake False BEFORE speaking.
        # This allows the main loop to return to wake mode.

        self.awake = False

        self.hud_state("SLEEPING")

        self.speak(
            "Going to sleep, boss. "
            "Say wake up Jarvis when you need me."
        )

        self.hud_state("SLEEPING")

        print()
        print("JARVIS IS NOW SLEEPING.")
        print("Say: Wake up Jarvis")


    # =========================================================
    # CONFIRMATION
    # =========================================================

    def confirm(self, question):

        self.speak(question)

        answer = self.listen(
            timeout=8,
            phrase_limit=5
        )

        if not answer:
            return False

        yes_words = [
            "yes",
            "yes jarvis",
            "confirm",
            "do it",
            "proceed",
            "okay",
            "ok",
            "sure"
        ]

        return any(
            word in answer
            for word in yes_words
        )


    # =========================================================
    # OPEN CHROME
    # =========================================================

    def get_chrome_path(self):

        chrome_paths = [

            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for path in chrome_paths:

            if os.path.exists(path):
                return path

        return None


    def open_chrome(self, url="https://www.google.com"):

        chrome = self.get_chrome_path()

        try:

            if chrome:

                subprocess.Popen(
                    [
                        chrome,
                        "--new-tab",
                        url
                    ]
                )

                return True

            # Fallback
            webbrowser.open_new_tab(url)

            return True

        except Exception as error:

            print(
                "CHROME ERROR:",
                error
            )

            return False


    # =========================================================
    # INSTALLED APP LAUNCHER
    # =========================================================

    def clean_app_name(self, name):

        name = name.lower().strip()

        prefixes = [
            "open ",
            "launch ",
            "start ",
            "run ",
            "please open ",
            "please launch ",
            "please start "
        ]

        for prefix in prefixes:

            if name.startswith(prefix):

                name = name[len(prefix):].strip()

                break

        # Common speech-recognition variations

        replacements = {
            "olama": "ollama",
            "vs code": "visual studio code",
            "visual studio": "visual studio code",
            "chrome browser": "google chrome",
            "google chrome browser": "google chrome",
            "ms word": "microsoft word",
            "ms excel": "microsoft excel",
            "ms powerpoint": "microsoft powerpoint",
            "power point": "microsoft powerpoint"
        }

        return replacements.get(
            name,
            name
        )


    def launch_from_start_menu(self, app_name):

        """
        Finds Windows Start Menu .lnk shortcuts.

        This allows commands such as:

        open spotify
        open discord
        open whatsapp
        open chrome
        open notepad
        open calculator
        open vscode 

        without hardcoding every application.
        """

        app_name = self.clean_app_name(
            app_name
        )

        if not app_name:
            return False

        start_menu_locations = [

            os.path.expandvars(
                r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
            ),

            os.path.expandvars(
                r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
            )
        ]

        normalized_query = re.sub(
            r"[^a-z0-9]+",
            " ",
            app_name
        ).strip()

        query_words = normalized_query.split()

        candidates = []

        for root in start_menu_locations:

            if not os.path.exists(root):
                continue

            try:

                for current_root, dirs, files in os.walk(root):

                    for filename in files:

                        if not filename.lower().endswith(
                            ".lnk"
                        ):
                            continue

                        display_name = os.path.splitext(
                            filename
                        )[0]

                        normalized_name = re.sub(
                            r"[^a-z0-9]+",
                            " ",
                            display_name.lower()
                        ).strip()

                        score = 0

                        # Exact match
                        if normalized_name == normalized_query:

                            score = 100

                        # Query contained in app name
                        elif normalized_query in normalized_name:

                            score = 80

                        # All query words present
                        elif all(
                            word in normalized_name
                            for word in query_words
                        ):

                            score = 70

                        if score > 0:

                            candidates.append(
                                (
                                    score,
                                    os.path.join(
                                        current_root,
                                        filename
                                    )
                                )
                            )

            except Exception as error:

                print(
                    "START MENU SEARCH ERROR:",
                    error
                )

        if not candidates:
            return False

        candidates.sort(
            key=lambda item: item[0],
            reverse=True
        )

        shortcut = candidates[0][1]

        try:

            os.startfile(shortcut)

            return True

        except Exception as error:

            print(
                "APP LAUNCH ERROR:",
                error
            )

            return False


    def launch_app(self, app_name):

        """
        Attempts several ways to launch an application.

        Priority:

        1. Common direct Windows applications
        2. Start Menu shortcut
        3. Executable available in PATH
        """

        app_name = self.clean_app_name(
            app_name
        )

        if not app_name:
            return False

        # -----------------------------------------------------
        # COMMON WINDOWS APPLICATIONS
        # -----------------------------------------------------

        common_apps = {

            "notepad": [
                "notepad.exe"
            ],

            "calculator": [
                "calc.exe"
            ],

            "calc": [
                "calc.exe"
            ],

            "paint": [
                "mspaint.exe"
            ],

            "wordpad": [
                "write.exe"
            ],

            "file explorer": [
                "explorer.exe"
            ],

            "explorer": [
                "explorer.exe"
            ],

            "command prompt": [
                "cmd.exe"
            ],

            "cmd": [
                "cmd.exe"
            ],

            "powershell": [
                "powershell.exe"
            ],

            "task manager": [
                "taskmgr.exe"
            ]
        }

        if app_name in common_apps:

            try:

                subprocess.Popen(
                    common_apps[app_name]
                )

                return True

            except Exception as error:

                print(
                    "COMMON APP ERROR:",
                    error
                )


        # -----------------------------------------------------
        # OLLAMA
        # -----------------------------------------------------

        if app_name in [
            "ollama"
        ]:

            try:

                subprocess.Popen(
                    ["ollama"]
                )

                return True

            except Exception:
                pass


        # -----------------------------------------------------
        # START MENU
        # -----------------------------------------------------

        if self.launch_from_start_menu(
            app_name
        ):

            return True


        # -----------------------------------------------------
        # DIRECT COMMAND / PATH
        # -----------------------------------------------------

        try:

            subprocess.Popen(
                app_name,
                shell=True
            )

            return True

        except Exception as error:

            print(
                "DIRECT APP ERROR:",
                error
            )

        return False


    # =========================================================
    # DIRECT COMMANDS
    # =========================================================

    def special_command(self, command):

        command = command.lower().strip()

        if not command:
            return False


        # =====================================================
        # SLEEP
        # =====================================================

        sleep_commands = [

            "sleep",
            "sleep jarvis",
            "jarvis sleep",
            "go to sleep",
            "jarvis go to sleep",
            "go into sleep",
            "go into standby",
            "go on standby",
            "stand by",
            "standby"
        ]

        if (
            command in sleep_commands
            or any(
                command.startswith(
                    phrase + " "
                )
                for phrase in sleep_commands
            )
        ):

            print(
                "DIRECT SLEEP COMMAND DETECTED"
            )

            self.sleep()

            return True


        # =====================================================
        # OPEN NEW GOOGLE TAB
        # =====================================================

        if (
            "open new tab" in command
            or command == "new tab"
        ):

            if self.open_chrome(
                "https://www.google.com"
            ):

                self.speak(
                    "Google tab opened, boss."
                )

            else:

                self.speak(
                    "I couldn't open Google Chrome, boss."
                )

            return True


        # =====================================================
        # GOOGLE
        # =====================================================

        if command in [
            "google",
            "open google",
            "open google chrome"
        ]:

            if self.open_chrome(
                "https://www.google.com"
            ):

                self.speak(
                    "Google is open, boss."
                )

            else:

                self.speak(
                    "I couldn't open Google Chrome, boss."
                )

            return True


        # =====================================================
        # YOUTUBE
        # =====================================================

        if command in [
            "youtube",
            "open youtube"
        ]:

            if self.open_chrome(
                "https://www.youtube.com"
            ):

                self.speak(
                    "YouTube is open, boss."
                )

            else:

                self.speak(
                    "I couldn't open Google Chrome, boss."
                )

            return True


        # =====================================================
        # INSTAGRAM
        # =====================================================

        if command in [
            "instagram",
            "open instagram"
        ]:

            if self.open_chrome(
                "https://www.instagram.com"
            ):

                self.speak(
                    "Instagram is open, boss."
                )

            else:

                self.speak(
                    "I couldn't open Google Chrome, boss."
                )

            return True


        # =====================================================
        # SEARCH GOOGLE
        # =====================================================

        search_prefixes = [
            "search google for ",
            "google search for ",
            "search for "
        ]

        for prefix in search_prefixes:

            if command.startswith(prefix):

                query = command[
                    len(prefix):
                ].strip()

                if query:

                    url = (
                        "https://www.google.com/search?q="
                        + urllib.parse.quote_plus(
                            query
                        )
                    )

                    if self.open_chrome(url):

                        self.speak(
                            f"Searching Google for {query}, boss."
                        )

                    else:

                        webbrowser.open(url)

                        self.speak(
                            f"Searching Google for {query}, boss."
                        )

                    return True


        # =====================================================
        # TIME
        # =====================================================

        time_commands = [

            "time",
            "what is the time",
            "what's the time",
            "what time is it",
            "tell me the time",
            "current time"
        ]

        if command in time_commands:

            now = datetime.datetime.now()

            time_text = now.strftime(
                "%I:%M %p"
            ).lstrip("0")

            self.speak(
                f"The current time is {time_text}, boss."
            )

            return True


        # =====================================================
        # DATE
        # =====================================================

        date_commands = [

            "date",
            "what is the date",
            "what's the date",
            "tell me the date",
            "current date",
            "today's date",
            "todays date",
            "what day is it"
        ]

        if command in date_commands:

            now = datetime.datetime.now()

            date_text = now.strftime(
                "%A, %B %d, %Y"
            )

            self.speak(
                f"Today is {date_text}, boss."
            )

            return True


        # =====================================================
        # SHUTDOWN
        # =====================================================

        shutdown_commands = [

            "shutdown",
            "shut down",

            "shutdown pc",
            "shut down pc",

            "shutdown computer",
            "shut down computer",

            "shutdown my pc",
            "shut down my pc",

            "shutdown my computer",
            "shut down my computer",

            "turn off pc",
            "turn off computer",

            "turn off my pc",
            "turn off my computer",

            "laptop band kardo",
            "bye bye mujhe sona hai",

            "sojao jarvis bye bye"
            

            
        ]

        if command in shutdown_commands:

            confirmed = self.confirm(
                "Are you sure you want me to shut down the computer, boss?"
            )

            if confirmed:

                self.speak(
                    "Shutdown confirmed. Goodbye, boss."
                )

                try:

                    subprocess.Popen(
                        [
                            "shutdown",
                            "/s",
                            "/t",
                            "5"
                        ]
                    )

                except Exception as error:

                    print(
                        "SHUTDOWN ERROR:",
                        error
                    )

                return True

            self.speak(
                "Shutdown cancelled, boss."
            )

            return True


        # =====================================================
        # RESTART
        # =====================================================

        restart_commands = [

            "restart",
            "restart pc",
            "restart computer",
            "restart my pc",
            "restart my computer",
            "reboot",
            "reboot pc",
            "reboot computer"
        ]

        if command in restart_commands:

            confirmed = self.confirm(
                "Are you sure you want me to restart the computer, boss?"
            )

            if confirmed:

                self.speak(
                    "Restart confirmed, boss."
                )

                try:

                    subprocess.Popen(
                        [
                            "shutdown",
                            "/r",
                            "/t",
                            "5"
                        ]
                    )

                except Exception as error:

                    print(
                        "RESTART ERROR:",
                        error
                    )

                return True

            self.speak(
                "Restart cancelled, boss."
            )

            return True


        # =====================================================
        # STOP JARVIS
        # =====================================================

        stop_commands = [

            "go offline",
            "shutdown jarvis",
            "stop jarvis",
            "exit jarvis",
            "quit jarvis"
        ]

        if command in stop_commands:

            self.speak(
                "Going offline, boss."
            )

            self.running = False

            return True


        # =====================================================
        # LISTEN
        # =====================================================

        if command in [
            "listen",
            "jarvis listen",
            "start listening"
        ]:

            self.speak(
                "I'm listening, boss."
            )

            return True


        # =====================================================
        # OPEN APP
        #
        # This is intentionally BEFORE AI.
        #
        # Example:
        #
        # open notepad
        # open chrome
        # open spotify
        # open discord
        # open whatsapp
        # open vscode
        # open ollama
        #
        # =====================================================

        app_command_prefixes = [

            "open ",
            "launch ",
            "start ",
            "run "
        ]

        for prefix in app_command_prefixes:

            if command.startswith(prefix):

                app_name = command[
                    len(prefix):
                ].strip()

                # Don't treat these as generic apps
                blocked_apps = [

                    "google",
                    "google chrome",
                    "youtube",
                    "instagram",
                    "new tab"
                ]

                if app_name in blocked_apps:
                    break

                if app_name:

                    print(
                        "APP REQUEST:",
                        app_name
                    )

                    if self.launch_app(
                        app_name
                    ):

                        self.speak(
                            f"{app_name} is open, boss."
                        )

                        return True

                    # If it wasn't found, let the normal
                    # action system try it before AI.
                    break


        # =====================================================
        # NORMAL ACTIONS
        #
        # IMPORTANT:
        # Your existing music system is called here.
        # Do NOT remove this.
        #
        # This keeps:
        #
        # play music
        # play YouTube songs
        # open files
        # videos
        # existing actions
        #
        # working through actions.py.
        # =====================================================

        try:

            self.hud_state(
                "EXECUTING"
            )

            result = perform_action(
                command
            )

            if result:

                self.speak(
                    result
                )

                return True

        except Exception as error:

            print(
                "ACTION ERROR:",
                error
            )

        return False


    # =========================================================
    # PROCESS COMMAND
    # =========================================================

    def process_command(self, command):

        if not command:
            return

        print(
            "\nCOMMAND RECEIVED BY CONVERSATION:",
            repr(command)
        )

        # DIRECT COMMANDS ALWAYS FIRST
        handled = self.special_command(
            command
        )

        if handled:
            return


        # =====================================================
        # AI BRAIN
        #
        # ONLY UNKNOWN COMMANDS REACH HERE.
        # =====================================================

        self.hud_state(
            "PROCESSING"
        )

        print(
            "\nAsking local AI..."
        )

        try:

            answer = ask_ai(
                command
            )

            self.speak(
                answer
            )

        except Exception as error:

            print(
                "AI ERROR:",
                error
            )

            self.speak(
                "I'm having trouble accessing my AI brain, boss."
            )


    # =========================================================
    # CONVERSATION MODE
    # =========================================================

    def conversation(self):

        print()
        print("=" * 60)
        print("ENTERING CONVERSATION")
        print("JARVIS CONVERSATION MODE STARTED")
        print("=" * 60)

        while (
            self.running
            and self.awake
        ):

            command = self.listen(
                timeout=10,
                phrase_limit=10
            )

            if not command:
                continue

            self.process_command(
                command
            )


    # =========================================================
    # MAIN RUN LOOP
    # =========================================================

    def run(self):

        print()
        print("=" * 60)
        print("          J.A.R.V.I.S. CONTINUOUS CORE")
        print("=" * 60)

        print("RUN STATE:", self.running, self.awake, self.speaking)

        # =====================================================
        # IMPORTANT:
        #
        # If the outer wake system has already authenticated the
        # speaker, the core must skip wake-word verification and
        # immediately enter active conversation mode.
        # =====================================================

        if self.running and self.awake:
            print("ENTERING CONVERSATION")
            self.conversation()
            return

        # =====================================================
        # PERMANENT JARVIS LOOP
        # =====================================================

        while self.running:

            # -----------------------------------------------
            # SLEEP MODE
            # -----------------------------------------------

            if not self.awake:

                self.wait_for_wake()

            # -----------------------------------------------
            # CONVERSATION MODE
            # -----------------------------------------------

            if (
                self.running
                and self.awake
            ):

                print("RUN STATE:", self.running, self.awake, self.speaking)
                print("ENTERING CONVERSATION")
                self.conversation()

        # =====================================================
        # COMPLETELY STOPPED
        # =====================================================

        self.hud_state(
            "SLEEPING"
        )

        print()

        print(
            "JARVIS completely stopped."
        )