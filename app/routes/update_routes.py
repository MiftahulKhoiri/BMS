from flask import Blueprint, jsonify
from flask_login import current_user
import subprocess
import requests

update_bp = Blueprint("update", __name__, url_prefix="/update")

# RAW VERSION FILE dari GitHub kamu
GITHUB_RAW_VERSION = (
    "https://raw.githubusercontent.com/MiftahulKhoiri/BMS/main/core/version.py"
)

# --------------------------------------------------------------------------------
# CEK UPDATE – membandingkan versi lokal dengan versi yang ada di GitHub
# --------------------------------------------------------------------------------
@update_bp.get("/check")
def check_update():
    """
    Mengambil file version.py dari GitHub lalu membandingkan dengan versi lokal.
    Jika berbeda → update tersedia.
    """
    try:
        # Ambil versi online (text file)
        response = requests.get(GITHUB_RAW_VERSION)
        if response.status_code != 200:
            return jsonify({"error": "Tidak dapat mengambil versi dari GitHub"}), 500

        online_raw = response.text

        # Ambil versi lokal
        from core.version import APP_VERSION

        # Parse versi online
        # Format expected: APP_VERSION = "1.0.0"
        try:
            online_version = online_raw.split("=")[1].replace('"', '').strip()
        except:
            return jsonify({"error": "Format version.py di GitHub tidak valid"}), 500

        update_available = (online_version != APP_VERSION)

        return jsonify({
            "ok": True,
            "update_available": update_available,
            "current_version": APP_VERSION,
            "github_version": online_version
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# --------------------------------------------------------------------------------
# APPLY UPDATE – menarik update dari GitHub (git pull)
# --------------------------------------------------------------------------------
@update_bp.post("/apply")
def apply_update():
    """
    HANYA ROOT yang boleh update.
    Menjalankan perintah git pull untuk mengambil versi terbaru dari GitHub.
    """
    if not current_user.is_authenticated:
        return jsonify({"ok": False, "msg": "Anda harus login"}), 401

    if current_user.role != 3:
        return jsonify({"ok": False, "msg": "Hanya root yang boleh update"}), 403

    try:
        # Jalankan git pull
        result = subprocess.check_output(
            ["git", "pull", "origin", "main"],
            stderr=subprocess.STDOUT
        )
        output = result.decode()

        return jsonify({
            "ok": True,
            "msg": "Update berhasil diterapkan",
            "output": output
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "ok": False,
            "msg": "Gagal melakukan update",
            "error": e.output.decode()
        }), 500

    except Exception as e:
        return jsonify({
            "ok": False,
            "msg": "Kesalahan internal",
            "error": str(e)
        }), 500