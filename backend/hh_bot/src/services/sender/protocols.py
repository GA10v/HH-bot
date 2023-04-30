from abc import ABC, abstractmethod


class SenderProtocol(ABC):
    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        ...

    @abstractmethod
    async def send_message(self, msg: str, recipient: str) -> None:
        ...
