import uuid
import re
from faker import Faker
from fastapi import Request, Response, APIRouter, FastAPI
from mockapi.utils.logger import get_logger
from typing import Dict, Any, Tuple
from mockapi.services.graphql_handler import create_graphql_app
import json as fake_json

fake = Faker()
logger = get_logger("mock_manager")

MOCK_PREFIX_TEMPLATE = "/mocks/{api_id}"
MOCK_GRAPHQL_PREFIX_TEMPLATE = "/mocks/{api_id}/graphql"

def generate_api_id():
    return uuid.uuid4().hex[:6]

def sanitize_id(raw_id: str) -> str:
    """Sanitizes a string to be URL-friendly."""
    s = re.sub(r'\s+', '_', raw_id) # Replace spaces with underscores
    s = re.sub(r'[^\w-]', '', s)   # Remove all non-word chars except dash
    return s.strip('-_').lower()  # Clean up edges and lowercase

class MockManager:
    """Manages the lifecycle of dynamic mock APIs."""
    def __init__(self):
        self.active_mocks: Dict[str, APIRouter] = {}

    def _generate_mock_response(self, schema: Dict[str, Any]) -> Any:
        if schema.get("type") == "object" and "properties" in schema:
            return {prop: self._generate_mock_response(sub_schema) for prop, sub_schema in schema["properties"].items()}
        if schema.get("type") == "array" and "items" in schema:
            return [self._generate_mock_response(schema["items"]) for _ in range(fake.random_int(min=1, max=3))]
        
        field_type = schema.get("type", "string")
        if field_type == "string": return fake.word()
        if field_type == "integer": return fake.random_int(min=1, max=1000)
        if field_type == "number": return fake.pyfloat()
        if field_type == "boolean": return fake.pybool()
        return None

    def _get_response_example(self, details: Dict[str, Any], components: Dict) -> Tuple[Any, str]:
        resp_content = details.get("responses", {}).get("200", {}).get("content", {})
        mimetype = next(iter(resp_content.keys()), "application/json")
        
        if "application/json" in resp_content:
            content_schema = resp_content["application/json"].get("schema", {})
            if "$ref" in content_schema:
                try:
                    ref_path = content_schema["$ref"].split('/')
                    component_name = ref_path[-1]
                    component_schema = components.get("schemas", {}).get(component_name, {})
                    return self._generate_mock_response(component_schema), mimetype
                except (KeyError, IndexError):
                    pass # Fallback if ref is invalid
        
        return {"message": "ok", "id": str(uuid.uuid4())}, "application/json"
    
    def register_rest_api(self, app: FastAPI, schema: Dict[str, Any]) -> str:
        """Creates and registers a new REST mock API router."""
        raw_id = schema.get("info", {}).get("title", "mock_api")
        api_id = f"{sanitize_id(raw_id)}_{generate_api_id()}"

        router = APIRouter()
        paths = schema.get("paths", {})
        components = schema.get("components", {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue
                
                example, mimetype = self._get_response_example(details, components)
                
                async def mock_endpoint(request: Request, ex=example, mt=mimetype):
                    return Response(content=fake_json.dumps(ex, indent=2), media_type=mt, status_code=200)

                router.add_api_route(
                    path,
                    mock_endpoint,
                    methods=[method.upper()],
                    tags=[f"Mock API - {api_id}"],
                )
                logger.info(f"Registered mock route for {api_id}: {method.upper()} {path}")
        
        prefix = MOCK_PREFIX_TEMPLATE.format(api_id=api_id)
        app.include_router(router, prefix=prefix)
        self.active_mocks[api_id] = router
        return prefix

    def register_graphql_api(self, app: FastAPI, sdl: str) -> str:
        """Creates and registers a new GraphQL mock API application."""
        api_id = generate_api_id()
        prefix = MOCK_GRAPHQL_PREFIX_TEMPLATE.format(api_id=api_id)
        
        try:
            graphql_app = create_graphql_app(sdl)
            app.mount(prefix, graphql_app, name=f"graphql-{api_id}")
            logger.info(f"Mounted new GraphQL endpoint for {api_id} at {prefix}")
            return prefix
        except Exception as e:
            logger.error(f"Failed to create GraphQL app for {api_id}: {e}")
            raise RuntimeError(f"Failed to create GraphQL app: {e}")

    def get_endpoints_and_examples(self, schema: Any, api_type: str, mock_url: str) -> Tuple[list, dict]:
        endpoints = []
        examples = {}
        if api_type == "rest":
            paths = schema.get("paths", {})
            components = schema.get("components", {})
            for path, methods in paths.items():
                full_path = f"{mock_url}{path}"
                endpoints.append(full_path)
                # Just show an example for the first method
                if methods:
                    method, details = next(iter(methods.items()))
                    example, _ = self._get_response_example(details, components)
                    examples[full_path] = example
        else:
            endpoints.append(mock_url)
            examples[mock_url] = { "query": "{ someQuery { id name } }" }
        return endpoints, examples