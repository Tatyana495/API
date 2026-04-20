from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="llm-p")
    environment: str = Field(default="dev")

    jwt_secret_key: str = Field(default="change-me")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=60)

    sqlite_path: str = Field(default="app.db")

    openrouter_api_key: str = Field(default="")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1")
    openrouter_model: str = Field(default="openai/gpt-4o-mini")
    openrouter_referer: str = Field(default="http://localhost:8000")
    openrouter_title: str = Field(default="llm-p")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
print("OPENROUTER_API_KEY exists:", bool(settings.openrouter_api_key))
print("OPENROUTER_API_KEY len:", len(settings.openrouter_api_key or ""))
print("OPENROUTER_BASE_URL:", settings.openrouter_base_url)
print("OPENROUTER_MODEL:", settings.openrouter_model)