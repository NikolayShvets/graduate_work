from typing import Protocol

from schemas.message import Message


class Sender(Protocol):
    def send(self, message: Message) -> None: ...
