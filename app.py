import logging
import logging.config
import uvicorn
from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot

from bot.bot import bot
from bot.handlers import dp
from core.config import Settings, LogConfig
settings = Settings()
logging.config.dictConfig(LogConfig().dict())
log = logging.getLogger("exchange_bot")

app = FastAPI()
WEBHOOK_PATH = f"/bot/{settings.bot_token}"
WEBHOOK_URL = settings.webhook_url + WEBHOOK_PATH


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


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000, )
