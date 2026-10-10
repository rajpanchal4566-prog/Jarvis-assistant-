import speech_recognition as sr
import pyttsx3
import wave
import tempfile
import os

recognizer = sr.Recognizer()

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    print(f"JARVIS: {text}")

    engine.say(text)
    engine.runAndWait()


def listen(timeout=5, phrase_time_limit=8):
    """
    Listen to microphone and convert speech to text.
    """

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        except sr.WaitTimeoutError:
            return None

    try:

        text = recognizer.recognize_google(
            audio
        )

        print(f"YOU: {text}")

        return text.lower().strip()

    except sr.UnknownValueError:

        print("Could not understand speech.")

        return None

    except sr.RequestError as error:

        print("Speech recognition error:", error)

        return None


def record_audio(filename, duration=5):

    print()
    print("Speak normally for the voice enrollment...")
    print()

    with sr.Microphone(sample_rate=16000) as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("Recording...")

        audio = recognizer.record(
            source,
            duration=duration
        )

    wav_data = audio.get_wav_data(
        convert_rate=16000,
        convert_width=2
    )

    with open(filename, "wb") as file:
        file.write(wav_data)

    print("Saved:", filename)