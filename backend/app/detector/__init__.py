from typing import Optional

import numpy as np
import torch
from numpy import random

from .models.experimental import attempt_load
from .utils.datasets import letterbox
from .utils.general import check_img_size, non_max_suppression, scale_coords
from .utils.plots import plot_one_box
from .utils.square import square
from .utils.torch_utils import TracedModel, select_device


class Detector:
    def __init__(self, image_size: int, conf: float, weights: str = f"weights/best.pt"):
        self.conf = conf
        self.image_size = image_size
        self.device = select_device("")
        self.model = attempt_load(weights, map_location=self.device)
        self.stride = int(self.model.stride.max())
        self.imgsz = check_img_size(image_size, s=self.stride)
        self.model = TracedModel(self.model, self.device, image_size)
        if self.device != "cpu":
            self.model.half()
        self.vid_path, self.vid_writer = None, None
        self.names = self.model.module.names if hasattr(self.model, "module") else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]
        if self.device != "cpu":
            self.model(
                torch.zeros(1, 3, self.imgsz, self.imgsz)
                .to(self.device)
                .type_as(next(self.model.parameters()))
            )

    def detect(
        self, im0s: np.array, big_size: int
    ) -> (np.array, list[int], float, int, Optional[int]):
        img = letterbox(im0s, self.image_size, stride=self.stride)[0]
        img = np.ascontiguousarray(img[:, :, ::-1].transpose(2, 0, 1))
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.device != "cpu" else img.float()
        img /= 255.0

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        with torch.no_grad():
            pred = self.model(img, augment=False)[0]

        det = non_max_suppression(pred, self.conf, 0.45, classes=None, agnostic=False)[0]

        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()

        stones_coords = [
            [(int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))]
            for *xyxy, conf, cls in reversed(det)
        ]

        size_mass, mean_size, count, distance = square(im0s, stones_coords, big_size)

        return im0s, size_mass, mean_size, count, distance
