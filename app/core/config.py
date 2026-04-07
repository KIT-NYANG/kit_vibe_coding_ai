from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_size: str = "large-v3-turbo"
    device: str = "auto"
    compute_type: str = "float16"
    beam_size: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()