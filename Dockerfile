FROM python:3.11-slim

WORKDIR /app

# System deps for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.4

# Copy dependency files first for layer caching
COPY pyproject.toml poetry.lock* ./

# Install deps (no venv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY j3li/ ./j3li/
COPY schema_registry.json ./
COPY data/ ./data/

# Expose FastAPI port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=15s --timeout=5s --retries=5 --start-period=30s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the API
CMD ["uvicorn", "j3li.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
