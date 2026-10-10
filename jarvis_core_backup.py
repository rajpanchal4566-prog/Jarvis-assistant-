import time
import subprocess
import webbrowser
import speech_recognition as sr

from ai_brain import ask_ai
from actions import perform_action
from security import verify_user


class JarvisCore:

    def __init__(self, hud=None):

        self.hud = hud

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        # JARVIS starts asleep.
        self.awake = False

        # JARVIS process stays alive.
        self.running = True

        # True only while JARVIS is talking.
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

        safe_text = str(text)

        # Escape apostrophes for PowerShell.
        safe_text = safe_text.replace("'", "''")

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

            # IMPORTANT:
            # Wait until JARVIS completely finishes speaking.
            self.speech_process.wait()

        except Exception as error:

            print("SPEECH ERROR:", error)

        finally:

            self.speech_process = None

            # Small safety delay so the microphone doesn't
            # immediately hear the last part of JARVIS's voice.
            time.sleep(0.5)

            self.speaking = False

            if self.awake:
                self.hud_state("STANDBY")
            else:
                self.hud_state("SLEEPING")

    # =========================================================
    # NORMAL LISTEN
    # =========================================================

    def listen(self, timeout=10, phrase_limit=10):

        # NEVER listen while JARVIS is speaking.
        if self.speaking:

            return ""

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

        self.awake = False

        self.hud_state("SLEEPING")

        print()
        print("=" * 60)
        print("JARVIS IS SLEEPING")
        print("Say: Wake up Jarvis")
        print("=" * 60)

        try:

            with sr.Microphone() as source:

                # Calibrate once when entering wake mode.
                print("Calibrating microphone...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                print("Wake listener ready.")

                while (
                    self.running
                    and not self.awake
                ):

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

                        wake_words = [

                            "wake up jarvis",

                            "wake jarvis",

                            "hey jarvis",

                            "jarvis wake up",

                            "wakeup jarvis",

                            "wakeup jarvis"
                        ]

                        if any(
                            phrase in text
                            for phrase in wake_words
                        ):

                            self.awake = True

                            self.hud_state("WAKE")

                            self.speak(
                                "Yes, boss?"
                            )

                            return

                    except sr.UnknownValueError:

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
    # PUT JARVIS TO SLEEP
    # =========================================================

    def sleep(self):

        # IMPORTANT:
        # Change state BEFORE speaking.
        # This makes the main loop return to the wake listener.
        self.awake = False

        self.hud_state("SLEEPING")

        self.speak(
            "Going to sleep, boss. Say wake up Jarvis when you need me."
        )

        self.hud_state("SLEEPING")

        print()
        print("JARVIS is now sleeping.")
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
    # SPECIAL COMMANDS
    # =========================================================

    def special_command(self, command):

        command = command.lower().strip()

        # -----------------------------------------------------
        # JARVIS SLEEP
        # -----------------------------------------------------

        sleep_commands = [
            "go to sleep",
            "jarvis sleep",
            "sleep jarvis",
            "jarvis go to sleep",
            "go into sleep",
            "go into standby",
            "go on standby",
            "stand by",
            "standby",
            "sleep"
        ]

        if any(
            phrase in command
            for phrase in sleep_commands
        ):

            self.sleep()

            return True

        # -----------------------------------------------------
        # NEW TAB
        # -----------------------------------------------------

        if (
            "open new tab" in command
            or command == "new tab"
        ):

            webbrowser.open_new_tab(
                "about:blank"
            )

            self.speak(
                "New tab opened, boss."
            )

            return True
        # -----------------------------------------------------
        # GOOGLE
        # -----------------------------------------------------

        if command == "open google":

            webbrowser.open(
                "https://www.google.com"
            )

            self.speak(
                "Google is open, boss."
            )

            return True

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        if command.startswith(
            "search google for "
        ):

            query = command[
                len("search google for "):
            ].strip()

            if query:

                import urllib.parse

                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote_plus(query)
                )

                webbrowser.open(url)

                self.speak(
                    f"Searching Google for {query}, boss."
                )

                return True

        # -----------------------------------------------------
        # SHUTDOWN
        # -----------------------------------------------------

        shutdown_commands = [

            "shutdown computer",

            "shut down computer",

            "shutdown my computer",

            "shut down my computer",

            "turn off computer",

            "turn off my computer"
        ]

        if any(
            phrase in command
            for phrase in shutdown_commands
        ):

            confirmed = self.confirm(
                "Are you sure you want me to shut down the computer, boss?"
            )

            if confirmed:

                self.speak(
                    "Shutdown confirmed. Goodbye, boss."
                )

                subprocess.Popen(
                    [
                        "shutdown",
                        "/s",
                        "/t",
                        "5"
                    ]
                )

                self.running = False

                return True

            self.speak(
                "Shutdown cancelled, boss."
            )

            return True

        # -----------------------------------------------------
        # RESTART
        # -----------------------------------------------------

        restart_commands = [

            "restart computer",

            "restart my computer",

            "reboot computer",

            "reboot my computer"
        ]

        if any(
            phrase in command
            for phrase in restart_commands
        ):

            confirmed = self.confirm(
                "Are you sure you want me to restart the computer, boss?"
            )

            if confirmed:

                self.speak(
                    "Restart confirmed. I'll be back shortly, boss."
                )

                subprocess.Popen(
                    [
                        "shutdown",
                        "/r",
                        "/t",
                        "5"
                    ]
                )

                self.running = False

                return True

            self.speak(
                "Restart cancelled, boss."
            )

            return True

        # -----------------------------------------------------
        # GO OFFLINE
        # -----------------------------------------------------

        offline_commands = [

            "go offline",

            "jarvis go offline",

            "stop jarvis",

            "shutdown jarvis",

            "quit jarvis"
        ]

        if any(
            phrase in command
            for phrase in offline_commands
        ):

            self.speak(
                "Going offline, boss."
            )

            self.running = False

            return True

        # -----------------------------------------------------
        # LISTEN
        # -----------------------------------------------------

        if command in [

            "listen",

            "jarvis listen",

            "start listening"
        ]:

            self.speak(
                "I'm listening, boss."
            )

            return True

        # -----------------------------------------------------
        # ACTIONS.PY
        # -----------------------------------------------------

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

        handled = self.special_command(
            command
        )

        if handled:

            return

        # -----------------------------------------------------
        # AI BRAIN
        # -----------------------------------------------------

        self.hud_state(
            "PROCESSING"
        )

        print()
        print("Asking local AI...")

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
    # CONVERSATION
    # =========================================================

    def conversation(self):

        print()
        print("=" * 60)
        print("JARVIS IS AWAKE")
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

            # Sleep is handled immediately.
            if (
                "go to sleep" in command
                or "jarvis sleep" in command
                or "go on standby" in command
                or "stand by" in command
                or command == "standby"
            ):

                self.sleep()

                return

            self.process_command(
                command
            )

    # =========================================================
    # PERMANENT RUN LOOP
    # =========================================================

    def run(self):

        print()
        print("=" * 60)
        print("J.A.R.V.I.S. CONTINUOUS CORE")
        print("=" * 60)

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        try:

            self.speak(
                "Please authenticate your voice, boss."
            )

            authenticated = verify_user()

            if not authenticated:

                self.speak(
                    "Voice authentication failed. Access denied."
                )

                return

            self.speak(
                "Voice authentication successful."
            )

        except Exception as error:

            print(
                "SECURITY ERROR:",
                error
            )

            self.speak(
                "I could not access the voice security system."
            )

            return

        # -----------------------------------------------------
        # PERMANENT LOOP
        # -----------------------------------------------------

        while self.running:

            # ================================================
            # SLEEP MODE
            # ================================================

            if not self.awake:

                self.wait_for_wake()

            # ================================================
            # AWAKE MODE
            # ================================================

            if (
                self.running
                and self.awake
            ):

                self.conversation()

        # -----------------------------------------------------
        # COMPLETELY STOPPED
        # -----------------------------------------------------

        self.awake = False

        self.hud_state(
            "SLEEPING"
        )

        print()
        print("JARVIS completely stopped.")