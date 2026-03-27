from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    pinecone_api_key: str
    pinecone_index_name: str = "customerchat-kb"
    pinecone_environment: str = "us-east-1"
    database_url: str = "sqlite:///./customerchat.db"
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
