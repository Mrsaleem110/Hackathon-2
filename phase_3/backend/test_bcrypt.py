import bcrypt

# Test basic bcrypt functionality
try:
    password = "testpass"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print("Bcrypt hashing works!")
    print("Hashed password:", hashed)

    # Test verification
    is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
    print("Password verification:", is_valid)
except Exception as e:
    print(f"Bcrypt error: {e}")
    import traceback
    traceback.print_exc()