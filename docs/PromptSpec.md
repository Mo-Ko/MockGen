# Prompt File Specification for MockGen

MockGen uses `.prompt` files to define mock API endpoints, request/response schemas, and logic. This document explains the prompt DSL, structure, and best practices.

## Why Prompts?

- **Rapid API prototyping**
- **LLM-powered schema and data generation**
- **No backend code required**

## Basic Structure

A `.prompt` file is a YAML or simple DSL file describing one or more endpoints. Example:

```yaml
endpoint: /users
method: GET
response:
  - id: integer
  - name: string
  - email: string
```

## Supported Fields

- `endpoint`: Path (e.g. `/users`)
- `method`: HTTP verb (GET, POST, etc)
- `request`: (optional) Request schema
- `response`: Response schema (fields and types)
- `logic`: (optional) Custom logic or LLM instructions

## Example: POST with Request Body

```yaml
endpoint: /login
method: POST
request:
  - username: string
  - password: string
response:
  - token: string
  - expires_in: integer
```

## Advanced: Dynamic Logic

```yaml
endpoint: /weather
method: GET
logic: "Return a random weather report for a city."
response:
  - city: string
  - temperature: float
  - condition: string
```

## Tips

- Use clear field names and types
- Add `logic` for LLM-powered dynamic responses
- Multiple endpoints = multiple `.prompt` files

## See Also

- [../README.md](../README.md)
- [LLM-Integration.md](LLM-Integration.md)
