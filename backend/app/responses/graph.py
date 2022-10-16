from typing import Optional

from pydantic import BaseModel


class GraphResponse(BaseModel):
    time: Optional[str]
    size: Optional[float]
