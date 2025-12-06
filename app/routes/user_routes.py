from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from app.utils.role_required import role_required
from app.services.user_service import *
from app.utils.file_utils import save_file
import os

user_bp = Blueprint("users", __name__, url_prefix="/users")

# 🔥 hanya admin & root
@user_bp.get("/")
@login_required
@role_required(2)
def get_users():
    users = list_users(current_app.db_session_factory)
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "status": u.status
        } for u in users
    ])


# 🔥 hanya admin & root
@user_bp.post("/update/<int:user_id>")
@login_required
@role_required(2)
def update_user_data(user_id):
    data = request.json or {}
    ok, res = update_user(current_app.db_session_factory, user_id, data)
    return jsonify({"ok": ok, "data": res if ok else res})


# 🔥 upload foto profil
@user_bp.post("/upload-profile/<int:user_id>")
@login_required
def upload_profile(user_id):
    if "file" not in request.files:
        return jsonify({"ok": False, "msg": "tidak ada file"})

    file = request.files["file"]
    upload_dir = "app/static/uploads/profiles"
    os.makedirs(upload_dir, exist_ok=True)

    filename = save_file(file, upload_dir)

    ok, user = update_user(current_app.db_session_factory, user_id, {
        "profile_photo": filename
    })

    return jsonify({"ok": ok, "filename": filename})


# 🔥 upload background
@user_bp.post("/upload-background/<int:user_id>")
@login_required
def upload_background(user_id):
    if "file" not in request.files:
        return jsonify({"ok": False, "msg": "tidak ada file"})

    file = request.files["file"]
    upload_dir = "app/static/uploads/backgrounds"
    os.makedirs(upload_dir, exist_ok=True)

    filename = save_file(file, upload_dir)

    ok, user = update_user(current_app.db_session_factory, user_id, {
        "background_photo": filename
    })

    return jsonify({"ok": ok, "filename": filename})


# 🔥 hanya root yg boleh hapus user
@user_bp.delete("/delete/<int:user_id>")
@login_required
@role_required(3)
def remove_user(user_id):
    ok, res = delete_user(current_app.db_session_factory, user_id)
    return jsonify({"ok": ok, "msg": res})