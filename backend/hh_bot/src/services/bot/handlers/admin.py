from aiogram import Bot, Dispatcher, exceptions
from aiogram.types import Message
from core.config import settings
from core.logger import get_logger
from services.bot.keyboards.v1.admin import admin_kb
from services.bot.tg_bot import get_bot, get_dispatcher  # noqa: F401
from services.bot.utils.msg import AdminMsg as msg

logger = get_logger(__name__)


class AdminHandler:
    def __init__(self, bot: Bot, dispatcher: Dispatcher, db, parse_service) -> None:
        self.bot = bot
        self.dispatcher = dispatcher
        self.db = db
        self.parser = parse_service

    async def connect(self, message: Message) -> None:
        try:
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.WELCOME}',
                reply_markup=admin_kb,
            )
        except exceptions as ex:
            logger.error(f'[-] Except <{ex}>')
            await message.reply(f'{message.from_user.first_name}{msg.ON_EXCEPT}')

    async def dump_vacansies(self, message: Message) -> None:
        try:
            await message.delete()
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.ON_DUMP}',
            )
            await self.parser.get_dump()
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.ON_FINISH}',
                reply_markup=admin_kb,
            )
        except exceptions as ex:
            logger.error(f'[-] Except <{ex}>')
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.ON_EXCEPT} <{ex}>',
                reply_markup=admin_kb,
            )

    async def update_db(self, message: Message) -> None:
        try:
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.ON_UPDATE}',
                reply_markup=admin_kb,
            )
            await self.db.migrate()
        except exceptions as ex:
            logger.error(f'[-] Except <{ex}>')
            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=f'{message.from_user.first_name}{msg.ON_EXCEPT} <{ex}>',
                reply_markup=admin_kb,
            )

    def admin_handlers(self) -> None:
        self.dispatcher.register_message_handler(
            callback=self.connect,
            commands=[settings.bot.ADMIN_CONNECT],
            is_chat_admin=True,
        )
        self.dispatcher.register_message_handler(
            callback=self.dump_vacansies,
            commands=[settings.bot.ADMIN_DUMP],
            is_chat_admin=True,
        )
        self.dispatcher.register_message_handler(
            callback=self.update_db,
            commands=[settings.bot.ADMIN_UPDATE],
            is_chat_admin=True,
        )
        # self.dispatcher.register_message_handler(
        #     callback=self.update_db,  # TODO
        #     commands=[settings.bot.ADMIN_DISCONNECT],
        #     is_chat_admin=True,
        # )
