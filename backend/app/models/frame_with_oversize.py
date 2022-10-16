from dataclasses import dataclass


@dataclass
class FrameWithOversizeModel(object):
    id: str
    body: bytes
