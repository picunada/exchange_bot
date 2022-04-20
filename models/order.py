import datetime
from typing import Optional

from pydantic import BaseModel


class Order(BaseModel):
    id: Optional[int]
    amount: int
    rate: float
    withdraw_card: str
    is_paid: bool
    status_id: Optional[int]
    payment_url: Optional[str]
    created_at: datetime.datetime
