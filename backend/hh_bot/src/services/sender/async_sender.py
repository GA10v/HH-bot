from email.message import EmailMessage
from functools import lru_cache

from aiosmtplib import SMTP, SMTPException
from core.config import settings
from core.logger import get_logger
from services.sender.protocols import SenderProtocol

logger = get_logger(__name__)


class EmailSender(SenderProtocol):
    def __init__(self) -> None:
        self.server = settings.email.SMTP_SERVER
        self.port = settings.email.SMTP_PORT
        self.user = settings.email.USER
        self.password = settings.email.PASSWORD
        self.subject = settings.email.SUBJECT
        self.client = SMTP(
            hostname=self.server,
            port=self.port,
            password=self.password,
            username=self.user,
        )
        logger.info('[+] EmailSender init...')

    async def connect(self):
        await self.client.connect()

    async def disconnect(self) -> None:
        await self.client.quit()

    async def _connect(self) -> bool:
        if not self.client.is_connected:
            await self.connect()
        return self.client.is_connected

    async def send_message(self, msg: str, recipient: str) -> None:
        message = EmailMessage()
        message['From'] = self.user
        message['To'] = recipient
        message['Subject'] = self.subject
        message.set_content(msg)
        try:
            if await self._connect():
                await self.client.sendmail(
                    sender=self.user,
                    recipients=recipient,
                    message=message.as_string(),
                )
                logger.info(f'[+] Send email to {recipient}: msg: <{message.as_string()}>')
        except SMTPException as exc:
            logger.exception(f'[-] Exception {exc}')
            raise
        finally:
            await self.disconnect()


@lru_cache
def get_sender() -> SenderProtocol:
    return EmailSender()
