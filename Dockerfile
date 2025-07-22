
# Stage 1: Install Poetry
FROM python:3.10-slim AS builder-base
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Stage 2: Build frontend assets
FROM node:22-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 3: Build final production image
FROM python:3.10-slim AS final
LABEL maintainer="Mohsin Kokab <moko.lums@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency files and poetry from builder
COPY --from=builder-base /usr/local/bin/poetry /usr/local/bin/poetry
COPY --from=builder-base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY backend/pyproject.toml backend/poetry.lock* ./

# Configure poetry to create the virtual env inside the project directory
RUN poetry config virtualenvs.in-project true

# Create the virtual environment and install dependencies
RUN poetry install --no-interaction --no-root --only main

# Copy the rest of the application code
COPY --from=frontend-build /app/frontend/dist /app/static
COPY backend/src ./src

# Create the non-root user
RUN useradd --system --create-home app

# --- THE CRITICAL FIX ---
# Change the ownership of the entire application directory to the app user
# This is done AFTER all files are copied and BEFORE switching user.
RUN chown -R app:app /app

# Switch to the non-root user for runtime
USER app

EXPOSE 8000

# Use 'poetry run' to execute the command from within the virtual environment
CMD ["poetry", "run", "uvicorn", "mockapi.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
