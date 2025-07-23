# MockGen Architecture

This document explains the internal structure, key modules, and data flow of MockGen.

## High-Level Overview

MockGen is a modern web application with a decoupled frontend and backend. The entire stack is designed to be run locally for development or as a unified containerized application.

- **Frontend**: A **Vue.js** Single-Page Application (SPA) provides the user interface for generating APIs. It uses **Pinia** for state management and a dedicated service layer for API communication.
- **Backend**: A **FastAPI** server built on Python. It exposes a REST API for the frontend, manages the AI interaction, and dynamically serves the generated mock APIs.
- **AI Engine**: An abstraction layer that communicates with LLMs (GPT/Gemini) to generate API schemas based on structured prompt templates.

## Directory Structure

The project is organized into two main parts: `backend` and `frontend`.

```
MockGen/
├── .github/workflows/ci.yml # GitHub Actions CI Pipeline
├── backend/
│   ├── src/mockapi/
│   │   ├── api/             # FastAPI routers (defines HTTP endpoints)
│   │   ├── core/            # Configuration, lifespan manager, and core dependencies
│   │   ├── prompts/         # The "brains": structured AI prompt templates
│   │   ├── schemas/         # Pydantic models for request/response validation
│   │   └── services/        # The core application logic
│   ├── tests/               # Pytest tests
│   ├── pyproject.toml
│   ├── .env.example         # Example environment file
│   └── .env                 # Your actual environment file (not committed)
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable Vue components
│   │   ├── services/        # API service layer (axios wrapper)
│   │   └── stores/          # Pinia state management stores
│   └── package.json
├── docker-compose.yml
├── Dockerfile
```

## Key Backend Modules

The backend follows a clean, service-oriented architecture.

- `mockapi/main.py`: The main entry point for the FastAPI application. It initializes the app, sets up middleware, and uses a **lifespan manager** to create and cache service instances at startup.
- `mockapi/api/router.py`: Defines the primary API endpoints (`/generate`, `/history`). It handles request validation and delegates all business logic to the `GenerationService`.
- `mockapi/services/generation_service.py`: The **orchestrator** of the application. It contains the core business logic, coordinating between the AI client and the mock manager to generate, validate, and register a new mock API.
- `mockapi/services/ai_client.py`: The dedicated **AI connector**. Its sole responsibility is to build prompts from templates, communicate with the LLM providers (OpenAI/Gemini), and parse the structured JSON response.
- `mockapi/services/mock_manager.py`: The **state manager** for mock APIs. It dynamically creates and mounts new API routers onto the main FastAPI application at runtime.
- `mockapi/services/graphql_handler.py`: A specialized module that dynamically creates an executable GraphQL schema and mock resolvers using the `ariadne` library.
- `mockapi/core/config.py`: The single source of truth for all configuration, using Pydantic to manage both application constants and environment variables. Environment variables are loaded from `backend/.env` in local/dev, or injected by Docker Compose in containers.
- `mockapi/prompts/`: A directory containing the structured prompt templates that guide the AI's schema generation, forming the "intelligent" core of the application.

## Data Flow for API Generation

1.  A user submits a prompt from the **Vue.js frontend**.
2.  The request hits the `/generate` endpoint in `api/router.py`.
3.  The router validates the request and calls the `GenerationService`.
4.  `GenerationService` orchestrates the process, first calling the `ai_client.py`.
5.  `AIClient` selects the appropriate prompt from the `prompts/` directory, formats it, and sends it to the selected LLM.
6.  The LLM returns a structured JSON response. `AIClient` parses this and returns a clean schema object (OpenAPI dict or GraphQL string).
7.  `GenerationService` receives the schema, validates its integrity, and passes it to the `MockManager`.
8.  `MockManager` dynamically creates a new FastAPI router (or mounts a GraphQL app) for the mock API and attaches it to the main application.
9.  A success response, including the URL of the new mock API, is sent back to the frontend.
