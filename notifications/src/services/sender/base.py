from typing import Protocol


class Sender(Protocol):
    def send(self) -> None: ...
