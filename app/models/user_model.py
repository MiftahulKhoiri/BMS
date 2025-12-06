from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, DateTime
from sqlalchemy.orm import registry, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

# Inisialisasi registry dan metadata - tetap pertahankan di global scope
mapper_registry = registry()
metadata = MetaData()  # Pastikan ini ada

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(150), unique=True, nullable=False),
    Column("email", String(255), unique=True),
    Column("password_hash", String(255), nullable=False),
    Column("role", Integer, default=1),  # 1=user, 2=admin, 3=root

    # ----------- KOLOM TAMBAHAN LENGKAP -----------
    Column("full_name", String(255)),
    Column("profile_photo", String(255)),    # foto profil
    Column("background_photo", String(255)), # foto background
    Column("phone", String(50)),
    Column("address", String(255)),
    Column("status", String(50), default="active"),

    # Perbaiki tipe data
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
    Column("last_login", DateTime, nullable=True),
)

@mapper_registry.mapped
class User:
    __table__ = users_table
    __allow_unmapped__ = True  # Untuk menghindari error type annotation

    # Flask-login property
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == "active"

    @property
    def is_anonymous(self):
        return False
    
    # Helper untuk role
    @property
    def is_admin(self):
        return self.role >= 2
    
    @property
    def is_root(self):
        return self.role == 3

    def __repr__(self):
        return f'<User {self.username}>'

# Pastikan untuk mengekspor metadata
__all__ = ['User', 'metadata', 'users_table', 'mapper_registry']