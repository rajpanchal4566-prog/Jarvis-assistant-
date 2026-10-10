import speech_recognition as sr
import subprocess
import time

from hud import JarvisHUD


recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6


# ============================================================
# HUD
# ============================================================

HUD = None


def set_hud_state(state):

    global HUD

    if HUD is not None:

        try:
            HUD.set_state(state)

        except Exception as error:
            print("HUD ERROR:", error)


# ============================================================
# SPEAK
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
# WAKE WORD
# ============================================================

def wait_for_wake_word():

    set_hud_state("STANDBY")

    print("\n" + "=" * 50)
    print("💤 JARVIS STANDBY")
    print("🎤 Say: Hey Jarvis")
    print("=" * 50)

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        while True:

            try:

                audio = recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=4
                )

                text = recognizer.recognize_google(
                    audio
                ).lower()

                print("HEARD:", text)

                if (
                    "hey jarvis" in text
                    or "wake up jarvis" in text
                    or "wake jarvis" in text
                ):

                    set_hud_state("WAKE")

                    return

            except sr.UnknownValueError:

                continue

            except sr.RequestError:

                print(
                    "Speech recognition unavailable."
                )

                time.sleep(2)

            except Exception as error:

                print(
                    "WAKE ERROR:",
                    error
                )

                time.sleep(1)


# ============================================================
# START EXISTING JARVIS
# ============================================================

def start_jarvis():
 
    from jarvis_core import JarvisCore

    jarvis = JarvisCore(
        hud=HUD
    )

    jarvis.run()


# ============================================================
# MAIN
# ============================================================

def main():

    global HUD

    print("=" * 60)
    print("             J.A.R.V.I.S. WAKE SYSTEM")
    print("=" * 60)

    # --------------------------------------------------------
    # START HUD
    # --------------------------------------------------------

    def hud_thread():

        global HUD

        HUD = JarvisHUD()

        HUD.set_state("STANDBY")

        HUD.run()

    import threading

    thread = threading.Thread(
        target=hud_thread,
        daemon=True
    )

    thread.start()

    time.sleep(1)

    # --------------------------------------------------------
    # STARTUP
    # --------------------------------------------------------

    speak(
        "JARVIS standby system activated."
    )

    # --------------------------------------------------------
    # CONTINUOUS WAKE LOOP
    # --------------------------------------------------------

    while True:

        wait_for_wake_word()

        speak(
            "Yes, boss?"
        )

        set_hud_state("LISTENING")

        try:

            start_jarvis()

        except KeyboardInterrupt:

            print(
                "\nJARVIS stopped."
            )

            break

        except Exception as error:

            print(
                "\nJARVIS ERROR:",
                error
            )

            speak(
                "I encountered an error, boss."
            )

        set_hud_state("STANDBY")

        speak(
            "Returning to standby."
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nJARVIS manually stopped."
        )