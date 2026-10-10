from security import setup_voice

print()
print("=" * 50)
print("J.A.R.V.I.S. SECURITY SETUP")
print("=" * 50)
print()

print("🎙️ VOICE ENROLLMENT")
print()
print("You will have 25 seconds to record your voice.")
print()
print("During the recording:")
print("  • Speak normally")
print("  • Speak slowly sometimes")
print("  • Speak a little louder sometimes")
print("  • Use different sentences")
print("  • Keep your natural voice")
print("  • Stay reasonably close to the microphone")
print("  • Avoid background noise")
print()

input("Press ENTER when ready...")

success = setup_voice()

print()

if success:

    print("=" * 50)
    print("VOICE ENROLLMENT SUCCESSFUL")
    print("=" * 50)

else:

    print("=" * 50)
    print("VOICE ENROLLMENT FAILED")
    print("=" * 50)