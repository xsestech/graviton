from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class KSPSettings(BaseSettings):
    DATA_PATH: str = '../../data/'
    DATA_DELAY: float = 0.1
    WAIT_TIME: float = 2
    WARP_FACTOR: int = 4
    TARGET_PERIAPSIS: float = 250e3
    N_REQUESTS: int = 1000
    IS_CHEAT_ON: bool = False
    TIME_RANGE: float = 1  # В часах
    N_SPLITS: int = 10

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_ksp_settings():
    return KSPSettings()
