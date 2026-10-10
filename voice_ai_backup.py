import speech_recognition as sr
import subprocess

from ai_brain import ask_ai
from actions import perform_action
from security import verify_user


# ============================================================
# J.A.R.V.I.S. VOICE AI + HUD
# ============================================================

recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


# ============================================================
# HUD CONNECTION
# ============================================================

HUD = None


def set_hud_state(state):

    global HUD

    if HUD is None:
        return

    try:
        HUD.set_state(state)
    except Exception as error:
        print(f"HUD ERROR: {error}")


# ============================================================
# JARVIS SPEAK
# ============================================================

def speak(text):

    set_hud_state("SPEAKING")

    print(f"\nJARVIS: {text}")

    safe_text = str(text).replace("'", "''")

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Speak('{safe_text}')"
    )

    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            command
        ],
        check=False
    )

    set_hud_state("STANDBY")


# ============================================================
# LISTEN
# ============================================================

            
        
def listen():

    set_hud_state("LISTENING")

    try:

        with sr.Microphone() as source:

            print("\n🎙️ Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.3
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        # ====================================================
        # VERIFY SPEAKER
        #
        # No announcement here.
        # Authentication was already completed during wake.
        # ====================================================

        from security import verify_audio

        if not verify_audio(
            audio,
            announce=False
        ):

            print(
                "VOICE REJECTED - COMMAND IGNORED."
            )

            set_hud_state(
                "STANDBY"
            )

            return ""

        # ====================================================
        # TRANSCRIBE ONLY AFTER VOICE MATCH
        # ====================================================

        set_hud_state(
            "PROCESSING"
        )

        print(
            "🧠 Processing..."
        )

        text = recognizer.recognize_google(
            audio
        )

        print(
            f"YOU: {text}"
        )

        return text.lower().strip()

    except sr.WaitTimeoutError:

        set_hud_state(
            "STANDBY"
        )

        return ""

    except sr.UnknownValueError:

        set_hud_state(
            "STANDBY"
        )

        return ""

    except sr.RequestError:

        speak(
            "Speech recognition is currently unavailable, boss."
        )

        return ""

    except Exception as error:

        print(
            f"\nLISTEN ERROR: {error}"
        )

        set_hud_state(
            "STANDBY"
        )

        return ""


# ============================================================
# CONFIRMATION
# ============================================================

def get_confirmation():

    speak(
        "This action will affect your computer. "
        "Please say yes to confirm or no to cancel, boss."
    )

    answer = listen()

    if answer in [
        "yes",
        "yes jarvis",
        "confirm",
        "do it",
        "proceed"
    ]:

        return True

    return False


# ============================================================
# DANGEROUS ACTIONS
# ============================================================

def execute_dangerous_action(action):

    set_hud_state("EXECUTING")

    if action == "SHUTDOWN_REQUEST":

        speak(
            "You requested a system shutdown, boss."
        )

        if get_confirmation():

            speak(
                "Shutdown confirmed. Goodbye, boss."
            )

            subprocess.run(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    "5"
                ],
                check=False
            )

            return

        speak(
            "Shutdown cancelled, boss."
        )

        return

    if action == "RESTART_REQUEST":

        speak(
            "You requested a system restart, boss."
        )

        if get_confirmation():

            speak(
                "Restart confirmed. I'll be back shortly, boss."
            )

            subprocess.run(
                [
                    "shutdown",
                    "/r",
                    "/t",
                    "5"
                ],
                check=False
            )

            return

        speak(
            "Restart cancelled, boss."
        )

        return

    if action == "SLEEP_REQUEST":

        speak(
            "You requested sleep mode, boss."
        )

        if get_confirmation():

            speak(
                "Entering sleep mode, boss."
            )

            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Start-Sleep -Seconds 1; "
                    "Add-Type -AssemblyName System.Windows.Forms; "
                    "[System.Windows.Forms.Application]::SetSuspendState("
                    "'Suspend', $false, $false)"
                ],
                check=False
            )

            return

        speak(
            "Sleep mode cancelled, boss."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    global HUD

    print("=" * 60)
    print("              J.A.R.V.I.S. VOICE AI")
    print("=" * 60)

    # --------------------------------------------------------
    # Connect to HUD
    # --------------------------------------------------------

    try:

        from jarvis_master import JarvisMaster

        # The master controller already owns the HUD.
        # We locate it through the running master instance.

    except Exception:

        pass

    speak(
        "JARVIS voice system starting."
    )

    # --------------------------------------------------------
    # VOICE AUTHENTICATION
    # --------------------------------------------------------

    speak(
        "Please authenticate your voice, boss."
    )

    try:

        authenticated = verify_user()

    except Exception as error:

        print(
            "\nVOICE AUTHENTICATION ERROR:"
        )

        print(error)

        speak(
            "I could not access the voice security system."
        )

        return

    if not authenticated:

        speak(
            "Voice authentication failed. Access denied."
        )

        return

    # --------------------------------------------------------
    # ONLINE
    # --------------------------------------------------------

    speak(
        "Voice authenticated. Welcome back, boss."
    )

    speak(
        "I'm online. How can I assist you?"
    )

    # --------------------------------------------------------
    # COMMAND LOOP
    # --------------------------------------------------------

    while True:

        command = listen()

        if not command:

            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        exit_phrases = [
            "go to sleep",
            "go offline",
            "goodbye jarvis",
            "stop listening",
            "jarvis go offline",
            "jarvis stop listening"
        ]

        if any(
            phrase in command
            for phrase in exit_phrases
        ):

            speak(
                "Going offline, boss."
            )

            break

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        set_hud_state("EXECUTING")

        action_result = perform_action(
            command
        )

        # ----------------------------------------------------
        # DANGEROUS ACTION
        # ----------------------------------------------------

        if action_result in [
            "SHUTDOWN_REQUEST",
            "RESTART_REQUEST",
            "SLEEP_REQUEST"
        ]:

            execute_dangerous_action(
                action_result
            )

            continue

        # ----------------------------------------------------
        # NORMAL ACTION
        # ----------------------------------------------------

        if action_result:

            speak(
                action_result
            )

            continue

        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        set_hud_state("PROCESSING")

        print(
            "\n🧠 Asking local AI..."
        )

        answer = ask_ai(
            command
        )

        speak(
            answer
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n\nJARVIS manually stopped."
        )

    except Exception as error:

        print(
            "\nJARVIS ERROR:"
        )

        print(error)