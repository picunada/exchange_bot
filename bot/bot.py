from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core.config import Settings
from bot.buttons.menu import menu

settings = Settings()

storage = MemoryStorage()
bot = Bot(token=settings.bot_token)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=menu)
