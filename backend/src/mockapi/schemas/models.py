from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Natural language API description")
    api_type: str = Field(..., description="API type: rest or graphql")
    llm: str = Field(..., description="LLM backend: openai or gemini")

class GenerateResponse(BaseModel):
    # Renamed 'schema' to 'api_schema' to avoid Pydantic conflicts
    api_schema: Any = Field(..., description="The generated OpenAPI or GraphQL schema")
    mock_url: str = Field(..., description="The base URL for the generated mock API")
    endpoints: List[str]
    examples: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    detail: str