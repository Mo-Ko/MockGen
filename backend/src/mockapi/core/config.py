
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path
import os

class AppSettings:
    
    """
    Holds constants that define the application's logic and behavior.
    These are not expected to change between environments.
    """
    # AI Client Settings (from ai_client.py)
    OPENAI_MODEL: str = "gpt-4o"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    MAX_TOKENS_OPENAI: int = 2048
    MAX_TOKENS_GEMINI: int = 8192

    # Router Validation Settings (from router.py)
    MAX_PROMPT_LENGTH: int = 10000
    PROMPT_INJECTION_PATTERNS: List[str] = [
        r"ignore previous instructions", r"shut down",
        r"delete all", r"system:", r"admin:"
    ]

    # Project root and directories
    APP_ROOT: Path = Path(os.getenv("APP_ROOT", Path(__file__).resolve().parent.parent.parent.parent))
    PROMPTS_DIR: Path = APP_ROOT / "src" / "mockapi" / "prompts"

    # Logging settings
    LOG_DIR: Path = APP_ROOT / "src" / "mockapi" / "log"
    LOG_FILE: Path = LOG_DIR / "mockapi.log"
    SHOW_CONSOLE_LOG: bool = True

class EnvironmentSettings(BaseSettings):
    """
    Manages settings loaded from environment variables or a .env file.
    Provides validation, type-casting, and a single source for env config.
    """
    OPENAI_API_KEY: SecretStr | None = None
    GEMINI_API_KEY: SecretStr | None = None
    STATIC_DIR: str | None = None
    BASE_SCHEMA_DIR: str = "schemas"

    # Load .env file if APP_ROOT is not set
    if not os.getenv("APP_ROOT"):
        env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
    model_config = SettingsConfigDict(
        env_file=env_path if env_path.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Create singleton instances to be used throughout the application
app_settings = AppSettings()
