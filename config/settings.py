import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FrontierAtlas AI Intelligence Ingestion Engine"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = Field(
        default=f"sqlite:///{BASE_DIR / 'data' / 'frontier_atlas.db'}",
        description="SQLAlchemy database connection string"
    )
    REDIS_URL: Optional[str] = None

    # LLM Provider Keys & Models
    # Tier 1: Gemini Flash
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Tier 2: Groq Llama 3
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Tier 3: DeepSeek
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    # External APIs
    GITHUB_TOKEN: Optional[str] = None

    # Google Sheets Integration
    GOOGLE_SERVICE_ACCOUNT_JSON: Optional[str] = None
    GOOGLE_SHEET_ID: Optional[str] = None

    # Crawler Settings
    MAX_CONCURRENT_REQUESTS: int = 10
    PER_DOMAIN_CONCURRENCY: int = 3
    DEFAULT_TIMEOUT_SECONDS: int = 15
    CRAWL_MAX_RETRIES: int = 3
    BACKOFF_BASE_SECONDS: float = 1.0
    BACKOFF_MAX_SECONDS: float = 30.0

    # Freshness
    FRESHNESS_HOURS: int = 24

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    EXPORTS_DIR: Path = BASE_DIR / "data" / "exports"
    SAMPLES_DIR: Path = BASE_DIR / "data" / "samples"
    DOCS_DIR: Path = BASE_DIR / "docs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
