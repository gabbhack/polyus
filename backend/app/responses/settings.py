from pydantic import BaseModel


class SettingsResponse(BaseModel):
    big_size: int
