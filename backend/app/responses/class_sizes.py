from typing import Optional

from pydantic import BaseModel


class ClassSizesResponse(BaseModel):
    sizes: Optional[list[float]]
