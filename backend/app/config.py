"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables"""

    # App
    APP_NAME: str = "Recipe Image Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./recipe_platform.db"
    DB_POOL_SIZE: int = 10

    # Redis (optional for MVP)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_ENABLED: bool = False

    # NLP
    SPACY_MODEL: str = "en_core_web_sm"
    NLP_CONFIDENCE_THRESHOLD: float = 0.5

    # Images
    STATIC_DIR: str = "backend/static"
    IMAGES_DIR: str = "backend/static/images/techniques"
    PEXELS_API_KEY: Optional[str] = None  # For image download script

    # CORS (add production domains when deployed)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,https://*.vercel.app,https://*.onrender.com"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Paths
    TAXONOMY_PATH: str = "data/taxonomy/cooking_actions_taxonomy.json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
