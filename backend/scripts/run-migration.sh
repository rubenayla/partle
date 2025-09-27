#!/bin/bash
# Simple migration runner for production
cd /srv/partle/backend
source .venv/bin/activate
python -m alembic upgrade head