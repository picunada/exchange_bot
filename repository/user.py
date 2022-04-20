import datetime
from typing import List, Optional

from database import users
from models import User
from repository import BaseRepository


class UserRepository(BaseRepository):
    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: User) -> User:
        user = User(
            username=u.username,
            chat_id=u.chat_id,
            order_id=u.order_id,
            is_admin=u.is_admin,
            is_active=u.is_active,
            created_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update(self, id: int, u: User) -> User:
        user = User(
            username=u.username,
            chat_id=u.chat_id,
            order_id=u.order_id,
            is_admin=u.is_admin,
            is_active=u.is_active,
            created_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_chat_id(self, chat_id: str):
        query = users.select().where(users.c.chat_id == chat_id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
