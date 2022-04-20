from .connect import metadata, engine
from .order import orders
from .user import users
from .status import statuses

metadata.create_all(bind=engine)
