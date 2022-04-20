import sqlalchemy
from .connect import metadata
import datetime

users = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("chat_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("order_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("order.id"), nullable=True),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow())
)