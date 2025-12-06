from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import (
    register_user,
    authenticate_user,
    ensure_root_user
)
from app.models.user_model import User
from app import login_manager

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"ok": False, "msg": "Username & password wajib ada"}), 400

    ok, res = register_user(current_app.db_session_factory, username, password, email)
    if not ok:
        return jsonify({"ok": False, "msg": res}), 400

    return jsonify({"ok": True, "user_id": res.id})

@auth_bp.post("/login")
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    ok, res = authenticate_user(current_app.db_session_factory, username, password)
    if not ok:
        return jsonify({"ok": False, "msg": res}), 401

    login_user(res)
    return jsonify({"ok": True, "user_id": res.id, "is_root": res.is_root})

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True})

@auth_bp.post("/ensure-root")
def ensure_root():
    data = request.json or {}
    username = data.get("username", "root")
    password = data.get("password", "root123")

    ok, res = ensure_root_user(current_app.db_session_factory, username, password)
    if not ok:
        return jsonify({"ok": False, "msg": res}), 400

    return jsonify({"ok": True, "user_id": res.id})

@auth_bp.get("/me")
@login_required
def me():
    user = current_user
    return jsonify({
        "id": user.id,
        "username": user.username,
        "is_root": user.is_root
    })

@login_manager.user_loader
def load_user(user_id):
    Session = current_app.db_session_factory
    session = Session()
    try:
        return session.query(User).get(int(user_id))
    finally:
        session.close()

@auth_bp.post("/login")
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    ok, user = authenticate_user(current_app.db_session_factory, username, password)
    if not ok:
        return jsonify({"ok": False, "msg": user}), 401

    login_user(user)
    return jsonify({
        "ok": True,
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    })