from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL: str = "medium"
    NUM_WORKERS: int = 2
