from functools import lru_cache
from fastapi import Depends
from mockapi.core.config import EnvironmentSettings
from mockapi.services.ai_client import AIClient
from mockapi.services.mock_manager import MockManager

@lru_cache
def get_settings() -> EnvironmentSettings:
    return EnvironmentSettings()

@lru_cache
def get_ai_client(settings: EnvironmentSettings = Depends(get_settings)) -> AIClient:

    openai_key = settings.OPENAI_API_KEY.get_secret_value() if settings.OPENAI_API_KEY else None
    gemini_key = settings.GEMINI_API_KEY.get_secret_value() if settings.GEMINI_API_KEY else None
    
    return AIClient(openai_key=openai_key, gemini_key=gemini_key)

@lru_cache
def get_mock_manager() -> MockManager:
    return MockManager()

# dependencies.py (moved and refactored)

import os
from functools import lru_cache
from fastapi import Depends
from mockapi.core.config import EnvironmentSettings
from mockapi.services.ai_client import AIClient
from mockapi.services.mock_manager import MockManager

def get_settings() -> EnvironmentSettings:
    return EnvironmentSettings()

def get_ai_client(settings: EnvironmentSettings = Depends(get_settings)) -> AIClient:
    openai_key = settings.OPENAI_API_KEY.get_secret_value() if settings.OPENAI_API_KEY else None
    gemini_key = settings.GEMINI_API_KEY.get_secret_value() if settings.GEMINI_API_KEY else None
    return AIClient(openai_key=openai_key, gemini_key=gemini_key)

@lru_cache(maxsize=1)
def get_mock_manager() -> MockManager:
    return MockManager()