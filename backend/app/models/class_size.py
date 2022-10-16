from dataclasses import dataclass


@dataclass
class ClassSizeModel(object):
    sizes: list[int]
