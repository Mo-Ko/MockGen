from fastapi import FastAPI, HTTPException
from ariadne import gql
import aiofiles
import json
import os
import asyncio
from datetime import datetime

from mockapi.schemas.models import GenerateRequest, GenerateResponse
from mockapi.services.ai_client import AIClient
from mockapi.services.mock_manager import MockManager
from mockapi.core.config import EnvironmentSettings
from mockapi.utils.logger import get_logger

class GenerationService:
    def __init__(self, ai_client: AIClient, mock_manager: MockManager, settings: EnvironmentSettings):
        self.ai_client = ai_client
        self.mock_manager = mock_manager
        self.settings = settings
        self.logger = get_logger("generation_service")

    def _validate_schema(self, schema: object, api_type: str) -> bool:
        """Validates the generated schema for basic correctness."""
        if api_type == "rest":
            return isinstance(schema, dict) and "paths" in schema and "info" in schema
        if api_type == "graphql":
            if not isinstance(schema, str) or "type Query" not in schema:
                return False
            try:
                gql(schema)
                return True
            except Exception:
                return False
        return False

    async def _save_and_log(self, schema: object, req: GenerateRequest):
        """Saves the generated schema to a file and logs the generation event."""
        history_file = os.path.join(self.settings.BASE_SCHEMA_DIR, "history.json")
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dir_path = os.path.join(self.settings.BASE_SCHEMA_DIR, req.api_type)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{ts}.{'json' if req.api_type == 'rest' else 'graphql'}")
        
        try:
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                content = json.dumps(schema, indent=2) if req.api_type == "rest" else schema
                await f.write(content)
            
            entry = {"prompt": req.prompt, "timestamp": datetime.now().isoformat(), "api_type": req.api_type}
            history = []
            if os.path.exists(history_file):
                async with aiofiles.open(history_file, "r", encoding="utf-8") as f:
                    content = await f.read()
                    if content: history = json.loads(content)
            
            history.insert(0, entry)
            async with aiofiles.open(history_file, "w", encoding="utf-8") as f:
                await f.write(json.dumps(history, indent=2))
        except Exception as e:
            self.logger.error(f"Failed during file save or history log: {e}")

    async def create_and_register_api(self, app: FastAPI, base_url: str, gen_req: GenerateRequest) -> GenerateResponse:
        """The main orchestration method for generating and registering a mock API."""
        for attempt in range(2):
            try:
                ai_result = await self.ai_client.generate_schema(gen_req.prompt, gen_req.api_type, gen_req.llm)
                
                if self._validate_schema(ai_result, gen_req.api_type):
                    self.logger.info("AI response validated successfully.")
                    relative_path = self.mock_manager.register_rest_api(app, ai_result) if gen_req.api_type == "rest" else self.mock_manager.register_graphql_api(app, ai_result)
                    mock_url = f"{base_url}{relative_path}"
                    endpoints, examples = self.mock_manager.get_endpoints_and_examples(ai_result, gen_req.api_type, mock_url)
                    
                    await self._save_and_log(ai_result, gen_req)
                    
                    app.openapi_schema = None
                    app.openapi()
                    
                    return GenerateResponse(api_schema=ai_result, mock_url=mock_url, endpoints=endpoints, examples=examples)
                
                # If validation fails, log it and let the loop retry
                self.logger.warning(f"Validation failed for AI result on attempt {attempt + 1}. Retrying...")
                raise ValueError("AI returned an invalid or incomplete schema.")
            
            except Exception as e:
                self.logger.error(f"Generation failed on attempt {attempt + 1}: {e}")
                if attempt == 0:
                    await asyncio.sleep(1)
        
        # If both attempts fail, raise the final exception
        raise HTTPException(status_code=500, detail="AI service failed to generate a valid schema after multiple attempts. Please try again or rephrase your prompt.")