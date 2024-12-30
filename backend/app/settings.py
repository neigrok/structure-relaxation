from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL: str = "2023-12-03-mace-128-L1_epoch-199.model"
    NUM_WORKERS: int = 2
