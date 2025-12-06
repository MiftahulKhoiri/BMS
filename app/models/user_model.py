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
    Column("role", Integer, default=1),   # 1=user, 2=admin, 3=root
)


@mapper_registry.mapped
class User:
    __table__ = users_table
    role: int = mapped_column(Integer)
    id: int = mapped_column(Integer, primary_key=True)
    username: str = mapped_column(String(150))
    email: str = mapped_column(String(255))
    password_hash: str = mapped_column(String(255))
    is_root: bool = mapped_column(Boolean)

    # Flask-login support
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