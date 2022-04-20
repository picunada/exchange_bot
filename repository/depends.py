from typing import Optional

from fastapi import Depends

from database.connect import database
from models import User
from repository import UserRepository, OrdersRepository, StatusRepository


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_orders_repository() -> OrdersRepository:
    return OrdersRepository(database)


def get_status_repository() -> StatusRepository:
    return StatusRepository(database)


async def get_current_user(chat_id: str,
                           users: UserRepository = get_user_repository()
                           ) -> Optional[User]:
    user = await users.get_by_chat_id(chat_id)
    if User is None:
        return None
    return user
