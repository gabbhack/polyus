import logging

from fastapi import APIRouter

from app.config import config
from app.requests.settings import Settings
from app.responses.ok import OkResponse
from app.responses.settings import SettingsResponse

logger = logging.getLogger()
router = APIRouter()


@router.get("/settings")
def get_settings() -> SettingsResponse:
    return SettingsResponse(big_size=config.big_size)


@router.post("/settings")
def set_settings(settings: Settings) -> OkResponse:
    logger.debug("Setup new settings: %s", settings.dict())
    config.big_size = settings.big_size
    return OkResponse(ok=True)
