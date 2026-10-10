from security import setup_voice


print()
print("=" * 50)
print("J.A.R.V.I.S. SECURITY SETUP")
print("=" * 50)
print()

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