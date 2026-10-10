import time
import speech_recognition as sr
import pyttsx3

from security import verify_user


# ============================================================
# JARVIS BASIC ASSISTANT
# Python 3.13
# ============================================================

recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


# ------------------------------------------------------------
# TEXT TO SPEECH
# ------------------------------------------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):

    print(f"JARVIS: {text}")

    try:

        engine.say(text)
        engine.runAndWait()

    except Exception as error:

        print("TTS ERROR:", error)


# ------------------------------------------------------------
# LISTEN
# ------------------------------------------------------------

def listen():

    try:

        with sr.Microphone() as source:

            print()
            print("🎙️ JARVIS LISTENING...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=7
            )

        print("🔊 Processing...")

        text = recognizer.recognize_google(
            audio
        )

        print(f"YOU: {text}")

        return text.lower()

    except sr.WaitTimeoutError:

        print("No speech detected.")

        return ""

    except sr.UnknownValueError:

        print("I couldn't understand that.")

        return ""

    except sr.RequestError as error:

        print("Speech recognition error:", error)

        return ""

    except Exception as error:

        print("LISTEN ERROR:", error)

        return ""


# ------------------------------------------------------------
# WAKE WORD
# ------------------------------------------------------------

def wait_for_wake_word():

    print()
    print("=" * 50)
    print("J.A.R.V.I.S. IS STANDBY")
    print("=" * 50)
    print()
    print('Say "Wake up Jarvis"')


    while True:

        text = listen()

        if not text:
            continue

        if (
            "wake up jarvis" in text
            or
            "wake up" in text
            or
            "jarvis" in text
        ):

            print()
            print("⚡ WAKE WORD DETECTED")

            return True


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    print()
    print("=" * 60)
    print("              J.A.R.V.I.S.")
    print("=" * 60)
    print("Starting...")
    print()


    # Give Windows/audio devices a moment
    time.sleep(1)


    # --------------------------------------------------------
    # WAIT FOR WAKE WORD
    # --------------------------------------------------------

    wait_for_wake_word()


    # --------------------------------------------------------
    # VOICE AUTHENTICATION
    # --------------------------------------------------------

    speak(
        "Voice detected. Please identify yourself, boss."
    )

    authenticated = verify_user()


    if not authenticated:

        speak(
            "Access denied."
        )

        print()
        print("Returning to standby mode...")

        return


    # --------------------------------------------------------
    # ACCESS GRANTED
    # --------------------------------------------------------

    speak(
        "Access granted."
    )

    time.sleep(0.5)

    speak(
        "Online, boss. What would you like me to do?"
    )


    # --------------------------------------------------------
    # COMMAND LOOP
    # --------------------------------------------------------

    while True:

        command = listen()

        if not command:
            continue


        # Exit
        if (
            "go to sleep" in command
            or
            "sleep" in command
            or
            "goodbye" in command
            or
            "shutdown jarvis" in command
        ):

            speak(
                "Going into standby mode, boss."
            )

            break


        # Basic test commands
        if "hello" in command:

            speak(
                "Hello, boss."
            )

            continue


        if "how are you" in command:

            speak(
                "All systems are operational."
            )

            continue


        if "who are you" in command:

            speak(
                "I am Jarvis, your personal AI assistant."
            )

            continue


        speak(
            "I heard you say " + command
        )


# ------------------------------------------------------------
# START
# ------------------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("JARVIS stopped.")

    except Exception as error:

        print()
        print("JARVIS ERROR:")
        print(error)