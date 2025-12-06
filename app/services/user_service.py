from app.models.user_model import User
from app.services.db_service import get_session
from datetime import datetime

def list_users(session_factory):
    with get_session(session_factory) as session:
        return session.query(User).all()

def get_user(session_factory, user_id):
    with get_session(session_factory) as session:
        return session.query(User).filter(User.id == user_id).first()

def update_user(session_factory, user_id, data: dict):
    with get_session(session_factory) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.updated_at = datetime.now().isoformat()
        session.add(user)
        return True, user

def delete_user(session_factory, user_id):
    with get_session(session_factory) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        session.delete(user)
        return True, "deleted"