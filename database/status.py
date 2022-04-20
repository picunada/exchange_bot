import sqlalchemy
from .connect import metadata

status = sqlalchemy.Table(
    "status",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("status", sqlalchemy.String)
)
