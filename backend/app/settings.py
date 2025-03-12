from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MODEL: str = "medium"
    NUM_WORKERS: int = 2
    MPR_API_KEY: str = "dummy"
