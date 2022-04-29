import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from aiogram import types, Dispatcher, Bot
from tortoise.contrib.fastapi import register_tortoise

from models import Rates
from bot.bot import bot
from bot.handlers import dp
from core.logger import log
from core.config import Settings
from utils.check_rate import check_rates

settings = Settings()

app: FastAPI = FastAPI()
WEBHOOK_PATH = f"/bot/{settings.bot_token}"
WEBHOOK_URL = settings.webhook_url + WEBHOOK_PATH

register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/log_now")
def log_now():
    log.debug("/api/log_now starts")
    log.info("I'm logging")
    log.warning("some warnings")

    return {"result": "OK"}


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    log.info("Server started!")
    await check_rate()


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    log.info("Bye!")


@repeat_every(seconds=60 * 10)
async def check_rate():
    rate = check_rates()
    await Rates.create(rate=rate)
    await asyncio.sleep(60 * 11)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
