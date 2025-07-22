# Configuration Guide for MockGen

This guide explains all configuration options, environment variables, and override strategies for MockGen.

## Environment Variables

- `APP_ROOT`: Root directory for the app (default: `/app`)
- `PYTHONPATH`: Python import path (default: `/app/src`)
- `STATIC_DIR`: Where built frontend assets are served from (default: `/app/static`)
- `GENMOCK_PORT`: Port to expose (default: `8000`)
- `OPENAI_API_KEY`, `GEMINI_API_KEY`: LLM provider keys

## .env File

Copy `.env.example` to `.env` and set your secrets and overrides.

```
APP_ROOT=/app
PYTHONPATH=/app/src
STATIC_DIR=/app/static
GENMOCK_PORT=8000
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...your-key...
```

## Docker & Compose

- All env vars are passed into the container
- `docker-compose.override.yml` can override commands, volumes, ports for dev
- Hot-reload enabled in dev mode

## config.py

- Advanced backend config (logging, LLM provider, etc)
- Override via env vars or edit file

## Tips

- Use `.env` for secrets, not in code
- For production, set only needed env vars

## See Also

- [../README.md](../README.md)
- [Architecture.md](Architecture.md)
