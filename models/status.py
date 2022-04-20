from typing import Optional

from pydantic import BaseModel


class Status(BaseModel):
    id: Optional[int]
    status: str
