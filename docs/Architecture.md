# MockGen Architecture

This document explains the internal structure and module roles of MockGen.

## Overview

- **FastAPI Backend**: Serves all API and static content
- **LLM Engine**: Handles prompt parsing, schema generation, and dynamic logic via GPT/Gemini
- **React Frontend**: For prompt submission and endpoint management
- **Dockerized**: Multi-stage build for reproducibility

## Directory Structure

- `backend/`
  - `src/`: Main backend code
  - `schemas/`: Saved prompt and schema files
  - `pyproject.toml`: Backend dependencies
- `frontend/`
  - `src/`: React app
  - `package.json`: Frontend dependencies
- `docs/`: Documentation

## Key Modules

- `mock_engine.py`: LLM prompt parsing, schema & data generation
- `api_router.py`: FastAPI route registration
- `dynamic_routes.py`: Hot-reload endpoints from prompt files
- `graphql_handler.py`: (if present) GraphQL endpoint support
- `schemas/`: Stores prompt and generated schema files
- `main.py`: FastAPI app entrypoint

## Data Flow

1. User submits `.prompt` via frontend or file
2. Backend parses prompt, uses LLM to generate schema/logic
3. Endpoints are registered dynamically
4. Requests to endpoints return static or LLM-generated data

## See Also

- [../README.md](../README.md)
- [PromptSpec.md](PromptSpec.md)
- [LLM-Integration.md](LLM-Integration.md)
