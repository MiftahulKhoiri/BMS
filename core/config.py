from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    INSTANCE_DIR = BASE_DIR / "instance"
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'bms.db'}"
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "ubah_key_ini_ke_yang_lebih_aman"
    DEBUG = True