from abc import abstractmethod
from typing import Optional, Protocol

import cv2
import numpy as np


class FrameRepository(Protocol):
    @abstractmethod
    def next_frame(self) -> Optional[np.array]:
        raise NotImplementedError


class VideoFrameRepository(FrameRepository):
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        assert self.cap.isOpened()
        self.cap.read()

    def next_frame(self) -> Optional[np.array]:
        if self.cap.isOpened():
            # skip 10 frames
            for i in range(10):
                self.cap.grab()
            _, im = self.cap.read()
            return im
        return None
