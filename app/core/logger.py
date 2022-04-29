import logging.config

from core.config import Settings, LogConfig

settings = Settings()
logging.config.dictConfig(LogConfig().dict())
log = logging.getLogger("exchange_bot")