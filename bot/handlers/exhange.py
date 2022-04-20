from aiogram import types

from bot.bot import dp, bot


@dp.message_handler()
async def start_exchange(message: types.Message):
    if message.text == "Exchange":
        await bot.send_message(message.from_user.id, "Напишите")