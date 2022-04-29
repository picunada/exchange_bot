import typing

from aiogram.dispatcher.filters import BoundFilter
from models import Users
from core.config import Settings


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        user = await Users.get(chat_id=obj.from_user.id)
        return user.is_admin == self.is_admin
