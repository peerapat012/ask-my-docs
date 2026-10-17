import pytest

from app.models.user import User
from sqlalchemy.exc import IntegrityError

def test_create_user(session):
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User",
        display_name="Test"
    )
    
    session.add(user)
    session.flush()
    
    assert user.id is not None
    assert user.email == "test@example.com"
    

def test_unique_email_constraint(session):
    user1 = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User",
        display_name="Test"
    )
    
    user2 = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User 2",
        display_name="Test 2"
    )
    
    session.add(user1)
    session.flush()
    session.add(user2)
    with pytest.raises(IntegrityError):
        session.flush()
