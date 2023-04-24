from functools import lru_cache

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from core.config import settings


@lru_cache
def get_bot(token=settings.bot.TOKEN) -> Bot:
    return Bot(token=token)


@lru_cache
def get_dispatcher() -> Dispatcher:
    bot = get_bot()
    storage = MemoryStorage()
    return Dispatcher(bot=bot, storage=storage)
