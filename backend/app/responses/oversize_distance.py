from typing import Optional

from pydantic import BaseModel


class OversizeDistanceResponse(BaseModel):
    oversize_distance: Optional[int]
