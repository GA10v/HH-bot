from pathlib import Path
from datetime import date

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class PostgresSettings(BaseConfig):
    USER: str = ''
    PASSWORD: str = ''
    DB: str = ''
    HOST: str = 'localhost'
    PORT: int = 5432

    @property
    def uri(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class ParserSettings(BaseConfig):
    BASE_URL: str = 'https://api.hh.ru/vacancies'
    VACANCY_NAME: str = 'python'
    PAGINATE: int = 30
    TIMEDELTA: int = 1

    @property
    def filename(self):
        return f'{Path(__file__).parent.parent}/data/vacancies_{date.today()}.json'

    class Config:
        env_prefix = 'HHPARSER_'


class TGBotSettings(BaseConfig):
    TOKEN: str = ''
    URL: str = ''

    class Config:
        env_prefix = 'TELEGRAM_'


class EmailSettings(BaseConfig):
    """Class is being used to keep all settings."""

    USER: str = ''
    PASSWORD: str = ''
    SMTP_SERVER: str = 'smtp.yandex.ru'
    SMTP_PORT: int = 587

    class Config:
        """Configuration plugin."""

        env_prefix = 'EMAIL_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'HHBot'
    BASE_DIR = Path(__file__).parent.parent
    postgres: PostgresSettings = PostgresSettings()
    parser: ParserSettings = ParserSettings()
    bot: TGBotSettings = TGBotSettings()
    email: EmailSettings = EmailSettings()


settings = ProjectSettings()
