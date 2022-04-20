from aiogram import Dispatcher, Bot, types
from core.config import Settings
from bot.buttons.menu import menu

settings = Settings()

bot = Bot(token=settings.bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=menu)

