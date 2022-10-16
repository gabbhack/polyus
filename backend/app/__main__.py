import logging
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import main, settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(log_handler)

app = FastAPI()
app.include_router(settings.router)
app.include_router(main.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://gold.app.sosus.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
