# Testing Guide

## Quick Testing Commands

### Backend Testing
```bash
cd backend

# Test imports work
uv run python -c "from app.main import app"

# Run pytest tests (if configured)
uv run pytest tests/

# Manual API test
curl http://localhost:8000/v1/products/?limit=5
```

### Frontend Testing
```bash
cd frontend

# Build test - catches import errors!
npm run build

# Run tests (Vitest)
npm test

# Dev server
npm run dev
```

## What Each Test Catches

- `npm run build` - **Catches missing imports, TypeScript errors**
- `uv run python -c "from app.main import app"` - **Catches Python import errors**
- API endpoint tests - **Verify filtering and functionality works**

## Testing Mock-Data Filtering

The system filters out products with "mock-data" tag by default:

```bash
# Should NOT show mock-data products
curl http://localhost:8000/v1/products/

# Should show mock-data products
curl "http://localhost:8000/v1/products/?include_test_data=true"
```

## Before Deploying

Always run:
1. `cd frontend && npm run build` - Ensures frontend builds
2. `cd backend && uv run python -c "from app.main import app"` - Ensures backend imports work
3. Test the servers start successfully