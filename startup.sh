#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting Uvicorn server..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 80