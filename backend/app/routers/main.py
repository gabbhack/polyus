import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

from app.config import config
from app.detector import Detector
from app.iterators.main_frame import main_frame
from app.iterators.one_frame import one_frame
from app.repositories.average_graph import MemoryAverageGraphRepository
from app.repositories.class_sizes import MemoryClassSizesRepository
from app.repositories.count import MemoryCountRepository
from app.repositories.distance import MemoryDistanceRepository
from app.repositories.frame import VideoFrameRepository
from app.repositories.frame_with_oversize import MemoryFrameWithOversizeRepository
from app.responses.class_sizes import ClassSizesResponse
from app.responses.frame_with_oversize import FrameWithOversizeResponse
from app.responses.graph import GraphResponse
from app.responses.ok import OkResponse
from app.responses.oversize_distance import OversizeDistanceResponse

logger = logging.getLogger()
router = APIRouter()
detector = Detector(640, 0.2)
frame_repository = VideoFrameRepository(path=config.video_path)
frame_with_oversize_repository = MemoryFrameWithOversizeRepository()
average_graph_repository = MemoryAverageGraphRepository()
class_sizes_repository = MemoryClassSizesRepository()
count_repository = MemoryCountRepository()
distance_repository = MemoryDistanceRepository()
main_frame_iterator = main_frame(
    detector,
    frame_repository,
    frame_with_oversize_repository,
    average_graph_repository,
    class_sizes_repository,
    count_repository,
    distance_repository,
)


@router.get("/stream")
def stream() -> StreamingResponse:
    logger.debug("Start stream")
    return StreamingResponse(
        main_frame_iterator, media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/frame_with_oversize")
def frame_with_oversize() -> FrameWithOversizeResponse:
    frame_id = frame_with_oversize_repository.pop_from_queue()
    if frame_id:
        frame_url = f"http://{config.domain}/frame_with_oversize/{frame_id}.jpg"
        logger.debug("Return frame with oversize: %s", frame_url)
        return FrameWithOversizeResponse(frame_url=frame_url)
    else:
        logger.debug("Return none frame with oversize")
        return FrameWithOversizeResponse(frame_url=None)


@router.get("/frame_with_oversize/{uuid}.jpg")
def show_frame(uuid: str):
    frame = frame_with_oversize_repository.get(uuid)
    if frame:
        logger.debug("Return frame with oversize: %s", uuid)
        return StreamingResponse(
            one_frame(frame.body),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )
    logger.debug("Not found frame with oversize: %s", uuid)
    raise HTTPException(status_code=404, detail="Frame not found")


@router.post("/clear_oversize_queue")
def clear_oversize_queue() -> OkResponse:
    logger.debug("Clear oversize queue")
    frame_with_oversize_repository.clear()
    return OkResponse(ok=True)


@router.get("/average_graph")
def average_graph() -> GraphResponse:
    size = average_graph_repository.get()

    if size:
        return GraphResponse(time=datetime.now().strftime("%H:%M:%S"), size=size)
    return GraphResponse(time=None, size=None)


@router.get("/class_sizes")
def class_sizes() -> ClassSizesResponse:
    class_size = class_sizes_repository.percents()
    return ClassSizesResponse(sizes=class_size)


@router.get("/count_graph")
def count_graph():
    avg = count_repository.get()
    return GraphResponse(time=datetime.now().strftime("%H:%M:%S"), size=avg)


@router.get("/oversize_distance")
def oversize_distance() -> OversizeDistanceResponse:
    return OversizeDistanceResponse(oversize_distance=distance_repository.get())
