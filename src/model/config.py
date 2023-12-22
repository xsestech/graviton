from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    G: float = 6.6743e-11
    VENUS_R: float = 700e3
    VENUS_MASS: float = 1.2243980e23
    PROBE_MASS: float = 5600e3
    V0: float = 6.761e3
    H0: float = 251319
    TIME_RANGE: float = 3600
    TIME_STEP: float = 1e-2
    METHOD: str = 'RK45'

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_model_settings():
    return ModelSettings()
