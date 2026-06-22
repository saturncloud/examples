from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    composio_api_key: str
    composio_user_id: str
    model_name: str = "gpt-4o"
    
    # This tells pydantic to read from your .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()