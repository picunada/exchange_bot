import sqlalchemy
from .connect import metadata
import datetime

orders = sqlalchemy.Table(
    "order",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("amount", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("rate", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("withdraw_card", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_paid", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("status_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("status.id"), nullable=False),
    sqlalchemy.Column("payment_url", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow())
)
