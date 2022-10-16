from pydantic import BaseModel


class Settings(BaseModel):
    big_size: int
