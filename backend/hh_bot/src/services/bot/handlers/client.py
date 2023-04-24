from aiogram import Bot, Dispatcher, exceptions  # noqa: F401
from aiogram.types import Message  # noqa: F401
from core.config import settings  # noqa: F401
from core.logger import get_logger
from services.bot.keyboards.v1.client import client_kb  # noqa: F401
from services.bot.tg_bot import get_bot  # noqa: F401

logger = get_logger(__name__)


class ClientHandler:
    def __init__(self, bot: Bot, disp: Dispatcher, db, parse_service) -> None:
        self.bot = bot
        self.disp = disp
        self.db = db
