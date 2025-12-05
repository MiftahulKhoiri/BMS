# ==========================================
# File: app/routes/BMS_auth.py
# Modul: Autentikasi User BMS
# ==========================================

from flask import Blueprint, request, jsonify, session

# Blueprint khusus autentikasi
auth_bp = Blueprint("BMS_auth", __name__, url_prefix="/auth")


# ===========================================================
#  BMS - LOGIN USER
#  Deskripsi:
#      - Menerima username & password
#      - Validasi akun
#      - Menyimpan session user
# ===========================================================
@auth_bp.post("/login")
def BMS_login_user():
    """Proses login user dan menyimpan session."""
    
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    # TODO: Ganti dengan pengecekan database asli
    if username == "root" and password == "root":
        session["user_id"] = 1
        session["role"] = "root"
        return jsonify({"status": "ok", "msg": "Login ROOT berhasil"})

    return jsonify({"status": "error", "msg": "User tidak ditemukan"}), 401



# ===========================================================
#  BMS - REGISTER USER
#  Deskripsi:
#      - Mendaftarkan user baru
#      - Menyimpan akun ke database (nanti)
# ===========================================================
@auth_bp.post("/register")
def BMS_register_user():
    """Mendaftarkan user baru (contoh sederhana)."""
    
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    # TODO: Integrasi dengan database users
    return jsonify({
        "status": "ok",
        "msg": f"User '{username}' terdaftar (dummy)"
    })



# ===========================================================
#  BMS - LOGOUT USER
#  Deskripsi:
#      - Menghapus semua session user
#      - Mengembalikan status logout
# ===========================================================
@auth_bp.get("/logout")
def BMS_logout_user():
    """Menghapus session user dan keluar."""
    
    session.clear()
    return jsonify({"status": "ok", "msg": "Logout berhasil"})