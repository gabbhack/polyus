from abc import abstractmethod
from typing import Protocol

from app.models.class_size import ClassSizeModel


class ClassSizesRepository(Protocol):
    @abstractmethod
    def add(self, sized: ClassSizeModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> ClassSizeModel:
        raise NotImplementedError


class MemoryClassSizesRepository(ClassSizesRepository):
    def __init__(self):
        self.sizes: list[int] = [0, 0, 0, 0, 0, 0, 0]

    def add(self, sized: ClassSizeModel) -> None:
        for i, size in enumerate(sized.sizes[1:]):
            self.sizes[i] += size

    def get(self) -> ClassSizeModel:
        return ClassSizeModel(sizes=self.sizes)

    def percents(self) -> list[float]:
        count = sum(self.sizes)
        if count == 0:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        return [i / count for i in self.sizes]
