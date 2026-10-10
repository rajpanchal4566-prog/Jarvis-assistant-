import pyttsx3

print("Starting JARVIS voice...")

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

print("Available voices:")

for i, voice in enumerate(voices):
    print(i, voice.name)

print()
print("Speaking now...")

engine.say("Hello boss. JARVIS voice system is online.")
engine.runAndWait()

print("Speech finished.")