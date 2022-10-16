from abc import abstractmethod
from typing import Optional, Protocol

from app.models.frame_with_oversize import FrameWithOversizeModel


class FrameWithOversizeRepository(Protocol):
    @abstractmethod
    def add(self, frame: FrameWithOversizeModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, frame_id: str) -> Optional[FrameWithOversizeModel]:
        raise NotImplementedError

    @abstractmethod
    def pop_from_queue(self) -> Optional[FrameWithOversizeModel]:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError


class MemoryFrameWithOversizeRepository(FrameWithOversizeRepository):
    def __init__(self) -> None:
        self.queue: list[str] = []
        self.bodies: dict[str, FrameWithOversizeModel] = {}

    def add(self, frame: FrameWithOversizeModel) -> None:
        self.queue.append(frame.id)
        self.bodies[frame.id] = frame

    def get(self, frame_id: str) -> Optional[FrameWithOversizeModel]:
        return self.bodies.pop(frame_id, None)

    def pop_from_queue(self) -> Optional[str]:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def clear(self) -> None:
        self.queue.clear()
        self.bodies.clear()
