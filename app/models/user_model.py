from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import registry, mapped_column

mapper_registry = registry()
metadata = MetaData()

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

    Column("created_at", String(50)),
    Column("updated_at", String(50)),
    Column("last_login", String(50)),
)

@mapper_registry.mapped
class User:
    __table__ = users_table

    id: int = mapped_column(Integer, primary_key=True)
    username: str = mapped_column(String(150))
    email: str = mapped_column(String(255))
    password_hash: str = mapped_column(String(255))
    role: int = mapped_column(Integer)

    # kolom tambahan
    full_name: str = mapped_column(String(255))
    profile_photo: str = mapped_column(String(255))
    background_photo: str = mapped_column(String(255))
    phone: str = mapped_column(String(50))
    address: str = mapped_column(String(255))
    status: str = mapped_column(String(50))
    created_at: str = mapped_column(String(50))
    updated_at: str = mapped_column(String(50))
    last_login: str = mapped_column(String(50))

    # Flask-login property
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False