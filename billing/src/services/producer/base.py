from typing import Protocol


class Producer(Protocol):
    async def produce(self) -> None: ...
