from typing import Protocol


class Consumer(Protocol):
    async def consume(self) -> None: ...
