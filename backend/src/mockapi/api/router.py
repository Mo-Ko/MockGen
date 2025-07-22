import re
import json
import os
from fastapi import APIRouter, HTTPException, Depends, Request
from better_profanity import profanity
import aiofiles

from mockapi.schemas.models import GenerateRequest, GenerateResponse, ErrorResponse
from mockapi.services.ai_client import AIClient
from mockapi.services.mock_manager import MockManager
from mockapi.services.generation_service import GenerationService
from mockapi.core.dependencies import get_ai_client, get_mock_manager, get_settings
from mockapi.core.config import app_settings, EnvironmentSettings
from mockapi.utils.logger import get_logger

router = APIRouter()
logger = get_logger("mockapi_router")

def validate_request(request: GenerateRequest):
    if not request.prompt or request.api_type not in ("rest", "graphql") or request.llm not in ("openai", "gemini"):
        raise HTTPException(status_code=400, detail="Invalid input.")
    if len(request.prompt) > app_settings.MAX_PROMPT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Prompt is too long.")
    if profanity.contains_profanity(request.prompt):
        raise HTTPException(status_code=400, detail="Prompt contains inappropriate language.")
    if any(re.search(p, request.prompt.lower()) for p in app_settings.PROMPT_INJECTION_PATTERNS):
        raise HTTPException(status_code=400, detail="Prompt contains forbidden patterns.")
    if len(request.prompt.split()) < 4:
        raise HTTPException(status_code=400, detail="Prompt is too vague. Please describe your API in more detail.")

@router.post("/generate", response_model=GenerateResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_api(
    fastapi_req: Request,
    gen_req: GenerateRequest,
    ai_client: AIClient = Depends(get_ai_client),
    mock_manager: MockManager = Depends(get_mock_manager),
    settings: EnvironmentSettings = Depends(get_settings),
):
    validate_request(gen_req)
    
    generation_service = GenerationService(
        ai_client=ai_client,
        mock_manager=mock_manager,
        settings=settings
    )
    
    base_url = str(fastapi_req.base_url).rstrip('/')
    
    return await generation_service.create_and_register_api(
        app=fastapi_req.app,
        base_url=base_url,
        gen_req=gen_req
    )

@router.get("/history")
async def get_history(type: str = None, limit: int = 10, settings: EnvironmentSettings = Depends(get_settings)):
    history_file = os.path.join(settings.BASE_SCHEMA_DIR, "history.json")
    if not os.path.exists(history_file):
        return []
    try:
        async with aiofiles.open(history_file, "r", encoding="utf-8") as f:
            content = await f.read()
            if not content: return []
            history = json.loads(content)
        if type:
            history = [h for h in history if h.get("api_type") == type]
        return history[:limit]
    except Exception as e:
        logger.error(f"Failed to read history: {e}")
        return []