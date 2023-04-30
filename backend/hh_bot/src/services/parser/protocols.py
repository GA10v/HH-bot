from abc import ABC, abstractmethod


class ParserProtocol(ABC):
    @abstractmethod
    async def get_vacancies(self, page: int | None) -> None:
        ...

    @abstractmethod
    async def get_gather(self) -> None:
        ...

    @abstractmethod
    async def get_dump(self) -> None:
        ...
