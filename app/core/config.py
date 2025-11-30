from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl
from typing import List, Dict, Any

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    APP_ENV: str = "dev"
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    DB_CREATE_IF_MISSING: bool = True

    GITHUB_ORG: str
    GITHUB_REPO: str
    GITHUB_BRANCH: str = "main"
    GITHUB_PAT: str

    AZDO_ORG: str
    AZDO_PROJECT: str
    AZDO_PIPELINE_ID: int
    AZDO_PAT: str

    PDM_SERVICES_JSON: List[Dict[str, Any]]
    PDM_USER: str
    PDM_PASS: str

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    LOG_FILE_BASENAME: str = "app"
    LOG_ROTATION_MB: int = 20
    LOG_BACKUP_COUNT: int = 10
    LOG_EXPORTERS_JSON: List[str] = ["file"]

settings = Settings()  # type: ignore
