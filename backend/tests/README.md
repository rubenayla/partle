# Testing Guide

## Quick commands

### Backend
```bash
cd backend

# Ensure imports resolve
uv run python -c "from app.main import app"

# Run pytest suite
uv run pytest tests/

# Smoke test API
curl http://localhost:8000/v1/products/?limit=5
```

### Frontend
```bash
cd frontend

# Build to catch TypeScript/import errors
npm run build

# Run Vitest suite
npm test

# Manual verification server
npm run dev
```

## What each step catches
- `npm run build` – finds missing imports and TypeScript issues before deploy.
- `uv run python -c "from app.main import app"` – verifies backend import tree and env vars.
- API `curl` calls – confirm filters/flags behave as expected.

## Mock-data filtering checks

```bash
# Default response excludes mock-data products
curl http://localhost:8000/v1/products/

# Include mock/test entries when needed
curl "http://localhost:8000/v1/products/?include_test_data=true"
```

## Pre-deploy checklist
1. `cd frontend && npm run build`
2. `cd backend && uv run python -c "from app.main import app"`
3. Start backend + frontend locally and hit the main flows
