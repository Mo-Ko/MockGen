# Configuration Guide for MockGen

This guide explains all configuration options for MockGen, focusing on the backend.

## Primary Configuration: `.env` File

The primary method for providing secrets and environment-specific settings is via a `.env` file located in the `backend/` directory. You can create one by copying the example:

```bash
cd backend
cp .env.example .env
```

You **must** edit this file to add your API keys for the LLM providers you wish to use.

```dotenv
# backend/.env

# Add your secret API keys here. You only need to provide one.
OPENAI_API_KEY="sk-..."
GEMINI_API_KEY="ai..."
```

## Advanced Configuration: `config.py`

MockGen uses a robust, type-safe configuration system powered by Pydantic, located at `backend/src/mockapi/core/config.py`. This file is the single source of truth for all settings.

It defines two classes:
1.  `AppSettings`: Contains static application constants that define the application's core behavior, such as LLM model names and validation rules. These are not meant to be changed by the user.
2.  `EnvironmentSettings`: This class automatically reads from environment variables or the `.env` file. It validates their types and provides them to the application.

## All Environment Variables

The `EnvironmentSettings` class recognizes the following variables:

| Variable         | Description                                                      | Default      |
| ---------------- | ---------------------------------------------------------------- | ------------ |
| `OPENAI_API_KEY` | Your secret API key for OpenAI.                                  | `None`       |
| `GEMINI_API_KEY` | Your secret API key for Google's Gemini.                         | `None`       |
| `STATIC_DIR`     | The absolute path to the built frontend assets.                  | `None`       |
| `BASE_SCHEMA_DIR`| The directory where generated schemas and history are saved.     | `"schemas"`  |

## Docker & Docker Compose

When running via `docker-compose.yml`, the `env_file` directive automatically loads the `.env` file into the container. The `STATIC_DIR` is also explicitly set in the `docker-compose.yml` environment to `/app/static`, which is the correct path inside the container.
