import sqlalchemy
from .connect import metadata
import datetime

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow())
)