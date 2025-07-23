# LLM Integration in MockGen

This document explains how MockGen uses Large Language Models (LLMs) like OpenAI GPT and Google Gemini.

## Supported LLMs

- **OpenAI GPT** (3.5/4)
- **Google Gemini**

## Usage

- LLMs generate response schemas, fake data, and dynamic logic for endpoints
- Prompt files can include `logic` for custom instructions
- LLM selection is configurable via env or config

## Fallback Strategies

- If LLM is unavailable, fallback to static schemas or cached responses
- Errors are logged and surfaced in the frontend

## Expected Output

- JSON-compatible data matching the prompt schema
- Realistic, type-correct fake data

## Security & Limits

- API keys required for LLMs
- Rate limits and error handling in place

## See Also

- [../README.md](../README.md)
- [Architecture.md](Architecture.md)
