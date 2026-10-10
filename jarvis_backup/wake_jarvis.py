import speech_recognition as sr
import time
import subprocess

from voice_ai import main


recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6
recognizer.phrase_threshold = 0.3


def speak(text):

    print(f"\nJARVIS: {text}")

    safe_text = text.replace("'", "''")

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


def listen_for_wake_word():

    with sr.Microphone() as source:

        print("\n💤 JARVIS STANDBY")
        print("🎤 Say: Hey Jarvis")

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
                ).lower().strip()

                print(f"HEARD: {text}")

                if (
                    "hey jarvis" in text
                    or "hey jarvis" in text.replace(",", "")
                    or "wake up jarvis" in text
                    or "wake jarvis" in text
                ):

                    return True

            except sr.UnknownValueError:

                continue

            except sr.RequestError:

                print(
                    "⚠️ Speech recognition unavailable."
                )

                time.sleep(2)

            except Exception as error:

                print(
                    f"Wake-word error: {error}"
                )

                time.sleep(1)


def main_wake_system():

    print("=" * 60)
    print("             J.A.R.V.I.S. WAKE SYSTEM")
    print("=" * 60)

    speak(
        "JARVIS standby system activated."
    )

    while True:

        # ----------------------------------------------
        # WAIT FOR WAKE WORD
        # ----------------------------------------------

        listen_for_wake_word()

        # ----------------------------------------------
        # JARVIS ACTIVATED
        # ----------------------------------------------

        speak(
            "Yes, boss?"
        )

        print("\n⚡ JARVIS ACTIVATED")

        # ----------------------------------------------
        # START YOUR EXISTING JARVIS
        # ----------------------------------------------

        try:

            main()

        except KeyboardInterrupt:

            print(
                "\nJARVIS stopped."
            )

            break

        except Exception as error:

            print(
                f"\nJARVIS error: {error}"
            )

            speak(
                "I encountered an error, boss."
            )

        # ----------------------------------------------
        # RETURN TO STANDBY
        # ----------------------------------------------

        speak(
            "Returning to standby."
        )


if __name__ == "__main__":

    main_wake_system()