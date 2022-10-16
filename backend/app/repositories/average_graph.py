from abc import abstractmethod
from typing import Optional, Protocol

from app.models.average_graph import AverageGraphModel


class AverageGraphRepository(Protocol):
    @abstractmethod
    def add(self, graph: AverageGraphModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Optional[float]:
        raise NotImplementedError


class MemoryAverageGraphRepository(AverageGraphRepository):
    def __init__(self):
        self.queue: list[AverageGraphModel] = []

    def add(self, graph: AverageGraphModel) -> None:
        self.queue.append(graph)

    def get(self) -> Optional[float]:
        result = 0
        if len(self.queue) > 0:
            for i in self.queue:
                result += i.size
            queue = self.queue
            self.queue = []
            return result / len(queue)
        return None
