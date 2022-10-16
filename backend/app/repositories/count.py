from abc import abstractmethod
from typing import Protocol


class CountRepository(Protocol):
    @abstractmethod
    def add(self, count: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> float:
        raise NotImplementedError


class MemoryCountRepository(CountRepository):
    def __init__(self) -> None:
        self.queue: list[int] = []

    def add(self, count: int) -> None:
        self.queue.append(count)

    def get(self) -> float:
        queue = self.queue
        self.queue = []
        if len(queue) == 0:
            return 0
        return sum(queue) / len(queue)
