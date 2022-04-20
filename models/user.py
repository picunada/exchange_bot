import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    username: str
    chat_id: int
    order_id: Optional[int]
    is_admin: bool
    is_active: bool
    created_at: datetime.datetime
