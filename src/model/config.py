from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    G: float = 6.6743e-11
    VENUS_R: float = 6051.8e3
    VENUS_MASS: float = 4.867e24
    PROBE_MASS: float = 5600e3
    V0: float = 11.8e3
    H0: float = 248e3
    TIME_RANGE: float = 3600
    TIME_STEP: float = 1e-4
    METHOD: str = 'RK45'

    model_config = SettingsConfigDict(env_file='.env')
