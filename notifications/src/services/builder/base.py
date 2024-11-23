from typing import Protocol


class Builder(Protocol):
    def build(self) -> None: ...
