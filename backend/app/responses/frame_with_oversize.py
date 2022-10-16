from typing import Optional

from pydantic import BaseModel


class FrameWithOversizeResponse(BaseModel):
    frame_url: Optional[str]
