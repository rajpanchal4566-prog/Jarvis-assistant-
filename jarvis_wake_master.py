import speech_recognition as sr
import subprocess
import time
import threading

from hud import JarvisHUD
from security import verify_audio


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
# AUTHENTICATED WAKE WORD
# ============================================================

def wait_for_wake_word():

    set_hud_state("STANDBY")

    print("\n" + "=" * 60)
    print("💤 JARVIS IS SLEEPING")
    print("🎤 Say: Hey Jarvis")
    print("=" * 60)

    with sr.Microphone() as source:

        print("🎙️ Wake listener active.")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        while True:

            try:

                # ------------------------------------------------
                # LISTEN FOR POSSIBLE WAKE PHRASE
                # ------------------------------------------------

                audio = recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=4
                )

                text = recognizer.recognize_google(
                    audio
                ).lower()

                print(
                    "HEARD:",
                    text
                )

                # ------------------------------------------------
                # CHECK WAKE PHRASE
                # ------------------------------------------------

                wake_detected = (
                    "hey jarvis" in text
                    or
                    "wake up jarvis" in text
                    or
                    "wakeup jarvis" in text
                    or
                    "wake jarvis" in text
                    or
                    "jarvis wake up" in text
                    or 
                    "listen jarvis " in text 
                    or
                    "hello jarvis" in text
                    or
                    "hii jarvis" in text
                    or 
                    "jarvis uth jao " in text 
                    or
                    "uthja jarvis" in text
                    or
                    "subah ho gayi uthja jarvis" in text
                    or 
                    "suno jarvis " in text 
                    or
                    "how are you jarvis" in text
                    or
                    "i am back jarvis" in text
                    or 
                    "helloowwww jarvis" in text 

                )

                if not wake_detected:

                    continue

                print()
                print("=" * 60)
                print("🎤 WAKE PHRASE DETECTED")
                print("🔐 VERIFYING SPEAKER...")
                print("=" * 60)

                # ------------------------------------------------
                # IMPORTANT
                #
                # The SAME audio recording containing the wake
                # phrase is sent to voice authentication.
                #
                # No second recording is required.
                # ------------------------------------------------

                authenticated = verify_audio(
                    audio,
                    announce=False
                )

                # ------------------------------------------------
                # WRONG PERSON
                # ------------------------------------------------

                if not authenticated:

                    print()
                    print(
                        "🔒 WAKE REJECTED"
                    )

                    print(
                        "Voice authentication failed."
                    )

                    # Absolutely no HUD response.
                    # Do not speak.
                    # Do not start JARVIS.
                    # Simply continue listening.

                    set_hud_state("STANDBY")

                    continue

                # ------------------------------------------------
                # CORRECT PERSON
                # ------------------------------------------------

                print()
                print("=" * 60)
                print("🔓 WAKE AUTHENTICATION SUCCESSFUL")
                print("=" * 60)

                set_hud_state("WAKE")

                return True

            except sr.UnknownValueError:

                # Speech was not understandable.
                # Ignore it silently.

                continue

            except sr.RequestError:

                print(
                    "Speech recognition unavailable."
                )

                time.sleep(2)

            except Exception as error:

                print()
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

    # Outer wake auth has already succeeded.
    # Do not re-trigger voice authentication or the wake listener
    # inside JarvisCore.run() for this execution path.
    jarvis.running = True
    jarvis.awake = True

    jarvis.run()


# ============================================================
# HUD THREAD
# ============================================================

def start_hud():

    global HUD

    try:

        HUD = JarvisHUD()

        # Start completely hidden/sleeping.
        HUD.set_state("STANDBY")

        HUD.run()

    except Exception as error:

        print(
            "HUD THREAD ERROR:",
            error
        )


# ============================================================
# MAIN
# ============================================================

def main():

    global HUD

    print("=" * 60)
    print("             J.A.R.V.I.S. WAKE SYSTEM")
    print("=" * 60)

    print()
    print("💤 JARVIS starting in silent standby mode...")
    print("🔐 Voice authentication required to wake.")
    print()

    # --------------------------------------------------------
    # START HUD
    #
    # We still create the HUD because JarvisCore needs it.
    # But we DO NOT make JARVIS speak at startup.
    # --------------------------------------------------------

    thread = threading.Thread(
        target=start_hud,
        daemon=True
    )

    thread.start()

    time.sleep(1)

    # --------------------------------------------------------
    # NO STARTUP SPEECH
    #
    # IMPORTANT:
    #
    # We intentionally removed:
    #
    # speak("JARVIS standby system activated.")
    #
    # --------------------------------------------------------

    print(
        "🤫 JARVIS is waiting silently for your wake phrase."
    )

    # --------------------------------------------------------
    # CONTINUOUS WAKE LOOP
    # --------------------------------------------------------

    while True:

        try:

            # ------------------------------------------------
            # WAIT FOR:
            #
            # Wake phrase
            # +
            # Correct speaker
            #
            # ------------------------------------------------

            authenticated = wait_for_wake_word()

            if not authenticated:

                continue

            # ------------------------------------------------
            # ONLY NOW DOES JARVIS WAKE
            # ------------------------------------------------

            set_hud_state("WAKE")

            speak(
                "Yes, boss?"
            )

            set_hud_state(
                "LISTENING"
            )

            # ------------------------------------------------
            # START EXISTING JARVIS
            # ------------------------------------------------

            start_jarvis()

        except KeyboardInterrupt:

            print(
                "\nJARVIS stopped."
            )

            break

        except Exception as error:

            print()
            print(
                "JARVIS ERROR:",
                error
            )

            try:

                speak(
                    "I encountered an error, boss."
                )

            except Exception:

                pass

        # ----------------------------------------------------
        # RETURN TO SLEEP
        # ----------------------------------------------------

        set_hud_state(
            "STANDBY"
        )

        print()
        print(
            "💤 JARVIS has returned to standby."
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