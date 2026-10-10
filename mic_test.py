import speech_recognition as sr

print("=" * 50)
print("JARVIS MICROPHONE TEST")
print("=" * 50)

recognizer = sr.Recognizer()

# Make recognition less sensitive to small background noise
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

print("\nChecking microphones...\n")

try:
    microphones = sr.Microphone.list_microphone_names()

    for index, name in enumerate(microphones):
        print(f"[{index}] {name}")

except Exception as e:
    print("\nMICROPHONE ERROR:")
    print(e)
    input("\nPress ENTER to exit...")
    raise SystemExit


print("\nDefault microphone will be used.")
print("\nPreparing microphone...")
print("Please stay quiet for 2 seconds.")

try:

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=2
        )

        print("\nMicrophone calibrated.")
        print("--------------------------------")
        print("🎤 LISTENING...")
        print("Say: Hello Jarvis")
        print("--------------------------------")

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=7
        )

except sr.WaitTimeoutError:

    print("\nNo speech detected.")

    input("\nPress ENTER to exit...")
    raise SystemExit

except Exception as e:

    print("\nMICROPHONE RECORDING ERROR:")
    print(e)

    input("\nPress ENTER to exit...")
    raise SystemExit


print("\nAudio captured successfully.")
print("Converting speech to text...")

try:

    text = recognizer.recognize_google(audio)

    print("\n" + "=" * 50)
    print("SUCCESS!")
    print("=" * 50)
    print("You said:")
    print(text)
    print("=" * 50)

except sr.UnknownValueError:

    print("\nI received your audio, but couldn't understand it.")

    print("\nTry speaking:")
    print("  - closer to the laptop")
    print("  - a little louder")
    print("  - more slowly")

except sr.RequestError as e:

    print("\nInternet speech-recognition service error:")
    print(e)

except Exception as e:

    print("\nSPEECH ERROR:")
    print(e)


input("\nPress ENTER to close...")