import datetime
from typing import List, Optional

from database import statuses
from models import Status
from repository import BaseRepository


class StatusRepository(BaseRepository):
    async def get_all(self, limit: int = 25, skip: int = 0) -> List[Status]:
        query = statuses.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[Status]:
        query = statuses.select().where(statuses.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return Status.parse_obj(user)

    async def create(self, s: Status) -> Status:
        status = Status(
            status=s.status
        )
        values = {**status.dict()}
        values.pop("id", None)
        query = statuses.insert().values(**values)
        status.id = await self.database.execute(query)
        return status

    async def update(self, id: int, s: Status) -> Status:
        status = Status(
            id=id,
            status=s.status
        )

        values = {**status.dict()}

        values.pop("id", None)
        query = statuses.update().where(statuses.c.id == id).values(**values)
        await self.database.execute(query)
        return status

    async def get_by_status(self, desired_status: str):
        query = statuses.select().where(statuses.c.status == desired_status)
        status = await self.database.fetch_one(query)
        if status is None:
            return None
        return Status.parse_obj(status)
