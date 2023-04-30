import asyncio
import json
from datetime import datetime, timedelta
from functools import lru_cache

import aiohttp
import fake_useragent
from aiohttp.client_exceptions import ClientError
from core.config import settings
from core.logger import get_logger
from services.layer_models import Vacancy
from services.parser.protocols import ParserProtocol

logger = get_logger(__name__)


class HHParser(ParserProtocol):
    def __init__(
        self,
        url: str,
        vacancy_name: str,
        paginate: int,
        timedelta: int,
    ) -> None:
        self.ua = fake_useragent.UserAgent()
        self.url = url
        self.vacancy_name = vacancy_name
        self.paginate = paginate
        self.timedelta = timedelta
        logger.info('[+] HHParser init...')

    def _get_params(self, page: int | None = None) -> dict:
        date = (datetime.now() - timedelta(days=self.timedelta)).strftime('%Y-%m-%d')
        if page:
            return {
                'url': self.url,
                'headers': {
                    'User-agent': self.ua.random,
                },
                'params': {
                    'text': f'NAME:{self.vacancy_name}',
                    'page': page,
                    'per_page': self.paginate,
                    'date_from': f'{date}',
                },
            }
        return {
            'url': self.url,
            'headers': {
                'User-agent': self.ua.random,
            },
            'params': {
                'text': f'NAME:{self.vacancy_name}',
                'per_page': self.paginate,
                'date_from': f'{date}',
            },
        }

    @staticmethod
    def _prepare_data(data: dict) -> Vacancy:
        skills = ', '.join([skill['name'] for skill in data['key_skills']])
        return Vacancy(
            name=data['name'],
            link=data['alternate_url'],
            company=data['employer']['name'],
            area=data['area']['name'],
            experience=data['experience']['name'] if data['experience'] else 'не указан',
            salary=str(data['salary']['from']) if data['salary'] else 'не указана',
            skills=skills,
            timestamp=data['published_at'],
        )

    async def get_vacancies(self, page: int | None) -> None:
        params = self._get_params(page)
        async with aiohttp.ClientSession() as session:
            resp = await session.get(**params)
            if resp.status != 200:
                logger.info(f'[-] Response status: {resp.status}')

            try:
                vacancies_id = []
                soup = json.loads(await resp.text())['items']
                for item in range(len(soup)):
                    vacancies_id.append(soup[item]['id'])

                for id in vacancies_id:
                    async with session.get(
                        url=f'{self.url}/{id}',
                        headers={'User-agent': self.ua.random},
                    ) as resp:
                        data = json.loads(await resp.text())
                    self.vacancies.append(self._prepare_data(data).dict())
            except ClientError as exp:
                logger.exception(f'[-] Exception {exp}')
                raise exp

    async def get_gather(self) -> None:
        params = self._get_params()
        async with aiohttp.ClientSession() as session:
            resp = await session.get(**params)
        try:
            tasks = []
            pages = int(json.loads(await resp.text())['pages'])
            items = int(json.loads(await resp.text())['found'])
            for page in range(pages):
                task = asyncio.create_task(self.get_vacancies(page))
                tasks.append(task)
            logger.info(f'[+] Found {items} vacansies in {pages} pages')
            await asyncio.gather(*tasks)
        except ClientError as exp:
            logger.exception(f'[-] Exception {exp}')
            raise exp

    async def get_dump(self) -> None:
        self.vacancies = []
        try:
            logger.info('[+] Start searching...')
            await self.get_gather()

        except ClientError as exp:
            logger.exception(f'[-] Exception {exp}')
            raise exp

        finally:
            with open(settings.parser.filename, 'w', encoding='utf-8') as file:
                json.dump(self.vacancies, file, ensure_ascii=False, indent=4)
            logger.info(f'[+] Dump in {settings.parser.filename}')


@lru_cache
def get_parser() -> ParserProtocol:
    url = settings.parser.BASE_URL
    vacancy_name = settings.parser.VACANCY_NAME
    paginate = settings.parser.PAGINATE
    timedelta = settings.parser.TIMEDELTA
    return HHParser(url, vacancy_name, paginate, timedelta)
