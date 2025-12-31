import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models.user import User
from app.api.v1.auth import get_password_hash

# Create a test user directly in the database
try:
    print("Creating test user directly in database...")
    db = SessionLocal()

    # Check if user already exists
    existing_user = db.query(User).filter(User.username == "testuser").first()
    if existing_user:
        print("Test user already exists, deleting it...")
        db.delete(existing_user)
        db.commit()

    # Create new user
    hashed_password = get_password_hash("testpass")
    test_user = User(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=hashed_password
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    print(f"Test user created successfully with ID: {test_user.id}")
    db.close()
except Exception as e:
    print(f"Error creating test user: {e}")
    import traceback
    traceback.print_exc()
    try:
        db.close()
    except:
        pass