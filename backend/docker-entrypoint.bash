#!/bin/bash

set -e

while ! nc -z ${POSTGRES_SERVER} ${POSTGRES_PORT}; do
  echo "Waiting for postgres to start..."
  sleep 3
done
echo "Postgres started"

alembic upgrade head

uvicorn main:app --port 8000 --host 0.0.0.0 --proxy-headers
