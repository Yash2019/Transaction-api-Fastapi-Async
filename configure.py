from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DATABASE_URL: str
    SECREAT_KEY: str
    ALGORITHM: str = 'HS256'

    model_config=SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

config = Setting()