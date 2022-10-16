from datetime import datetime
from typing import Iterator
from uuid import uuid4

import cv2

from app.config import config
from app.detector import Detector
from app.models.average_graph import AverageGraphModel
from app.models.class_size import ClassSizeModel
from app.models.frame_with_oversize import FrameWithOversizeModel
from app.repositories.average_graph import AverageGraphRepository
from app.repositories.class_sizes import ClassSizesRepository
from app.repositories.count import CountRepository
from app.repositories.distance import DistanceRepository
from app.repositories.frame import FrameRepository
from app.repositories.frame_with_oversize import FrameWithOversizeRepository


def main_frame(
    detector: Detector,
    frame_repository: FrameRepository,
    frame_with_oversize_repository: FrameWithOversizeRepository,
    average_graph_repository: AverageGraphRepository,
    class_sizes_repository: ClassSizesRepository,
    count_repository: CountRepository,
    distance_repository: DistanceRepository,
) -> Iterator[bytes]:
    while True:
        original_frame = frame_repository.next_frame()
        if original_frame is not None:
            neuro_frame, sizes, average_size, count, distance = detector.detect(
                original_frame, config.big_size
            )
            success, buffer = cv2.imencode(".jpg", neuro_frame)
            if success:
                average_graph_repository.add(
                    AverageGraphModel(time=datetime.now().strftime("%H:%M"), size=average_size)
                )
                class_sizes_repository.add(ClassSizeModel(sizes))
                count_repository.add(count)
                distance_repository.save(distance)
                bytes_frame = buffer.tobytes()
                # if the oversized stones are greater than zero
                if sizes[0] > 0:
                    frame_with_oversize = FrameWithOversizeModel(id=str(uuid4()), body=bytes_frame)
                    frame_with_oversize_repository.add(frame_with_oversize)
                yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + bytes_frame + b"\r\n"
            else:
                # Cant encode to .jpg
                # Return zero byte
                yield b""
        else:
            # Cant get next frame from source
            # Stop stream
            yield b""
            break
