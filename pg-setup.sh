#!/bin/bash

# Step 1: Run Docker container for pgvector
docker run -d \
  --name pgvector \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=postgres \
  -p 5433:5432 \
  ankane/pgvector

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10  # Sleep for 10 seconds, adjust if needed

# Step 2: Create a new database and install the vector extension
psql -h localhost -p 5433 -U postgres -d postgres << EOF
CREATE DATABASE ragdb;
CREATE EXTENSION IF NOT EXISTS vector;
\q
EOF

# Step 3: Start the FastAPI server
# echo "Starting FastAPI server..."
# python -m uvicorn main:app --port 8000
