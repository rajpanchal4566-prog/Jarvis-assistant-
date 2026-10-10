from security import verify_user


print()
print("Starting voice test...")
print()

result = verify_user()

print()
print("================================")
print("FINAL RESULT")
print("================================")

if result:
    print("ACCESS GRANTED")
else:
    print("ACCESS DENIED")