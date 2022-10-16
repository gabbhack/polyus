from pydantic import BaseSettings


class Config(BaseSettings):
    domain: str
    big_size: int
    video_path: str


config = Config()
