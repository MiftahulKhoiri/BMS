from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
from app.services.db_service import get_session

def register_user(session_factory, username, password, email=None, is_root=False):
    with get_session(session_factory) as session:
        existing = session.query(User).filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing:
            return False, "Username atau email sudah ada"

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed, is_root=is_root)
        session.add(user)
        session.flush()
        return True, user

def authenticate_user(session_factory, username, password):
    with get_session(session_factory) as session:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            return False, "User tidak ditemukan"

        if check_password_hash(user.password_hash, password):
            return True, user

        return False, "Password salah"

def ensure_root_user(session_factory, username="root", password="root123"):
    with get_session(session_factory) as session:
        root = session.query(User).filter(User.is_root == True).first()
        if root:
            return False, "Root sudah ada"

        hashed = generate_password_hash(password)
        user = User(username=username, password_hash=hashed, is_root=True)
        session.add(user)
        session.flush()
        return True, user

def create_root_if_not_exists(session_factory):
    with get_session(session_factory) as session:
        root = session.query(User).filter(User.role == 3).first()
        if root:
            return False, "Root sudah ada"

        root = User(
            username="root",
            email="root@bms.local",
            password_hash=generate_password_hash("root123"),
            role=3
        )
        session.add(root)
        session.flush()
        return True, root