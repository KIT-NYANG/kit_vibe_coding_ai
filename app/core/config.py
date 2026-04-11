from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # STT
    model_size: str = "large-v3-turbo"
    device: str = "auto"
    compute_type: str = "float16"
    beam_size: int = 5

    # Summary
    openai_api_key: str
    summary_model: str = "gpt-5.4"
    summary_temperature: float = 0.2

    #analysis
    openai_api_key: str
    llm_model: str = "gpt-5.4"
    llm_temperature: float = 0.2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()