from typing import Literal

from pydantic import BaseModel


class OkResponse(BaseModel):
    ok: Literal[True]
