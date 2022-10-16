from abc import abstractmethod
from typing import Optional, Protocol


class DistanceRepository(Protocol):
    @abstractmethod
    def save(self, distance: Optional[int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Optional[int]:
        raise NotImplementedError


class MemoryDistanceRepository(DistanceRepository):
    def __init__(self):
        self.last: Optional[int] = None

    def save(self, distance: Optional[int]) -> None:
        self.last = distance

    def get(self) -> Optional[int]:
        return self.last
