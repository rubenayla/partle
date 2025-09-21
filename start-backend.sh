#!/bin/bash
cd /srv/partle/backend
export PATH="/home/deploy/.local/bin:$PATH"
export DATABASE_URL="postgresql://partle_user:partle_secure_password@localhost/partle"
export ELASTICSEARCH_HOST="localhost"
export ELASTICSEARCH_PORT="9200"
export ELASTICSEARCH_INDEX="products"
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
