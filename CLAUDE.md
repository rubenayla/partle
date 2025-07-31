# Partle Project - Claude Notes

## Project Structure
- **Backend**: Python FastAPI application using Poetry for dependency management
- **Frontend**: React/TypeScript application using npm/Node.js
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations

## Backend Commands (run from `/backend` directory)
- **Run migrations**: `poetry run alembic upgrade head`
- **Create migration**: `poetry run alembic revision -m "description"`
- **Check migration status**: `poetry run alembic current`
- **Run Python scripts**: `poetry run python <script>`

## Frontend Commands (run from `/frontend` directory)
- **Install dependencies**: `npm install`
- **Run dev server**: `npm run dev`
- **Run tests**: `npm test`
- **Build**: `npm run build`

## Key Files
- **Backend models**: `backend/app/db/models.py`
- **Backend schemas**: `backend/app/schemas/`
- **Alembic migrations**: `backend/alembic/versions/`
- **Poetry config**: `backend/pyproject.toml`
- **Frontend config**: `frontend/package.json`

## Database Notes
- Uses PostgreSQL enums for StoreType: 'physical', 'online', 'chain'
- Recent migration `8cdfc51661a9` fixed enum update issues by using proper SQL sequence
- SQLAlchemy models may need app restart after enum changes

## Testing
- **Backend**: pytest (check for test commands in pyproject.toml)
- **Frontend**: Vitest (configured in vite.config.js)
- **Search Engine**: `poetry run python test_search_quick.py` (quick verification)
- **Search Tests**: `poetry run pytest app/tests/test_search_simple.py -v` (comprehensive)

## API Standards
- **ALWAYS use trailing slash** for all API endpoints: `/v1/stores/`, `/v1/products/`, `/v1/auth/`
- Base URL: `http://localhost:8000` (from VITE_API_BASE in .env.local)

## Search Engine
- **Elasticsearch** for scalable search (millions of products)
- **Setup**: `docker compose up -d elasticsearch && poetry run python manage_search.py setup`
- **New endpoint**: `/v1/search/products/` with advanced filtering
- **Fallback**: `/v1/products/` uses database search if Elasticsearch unavailable

## Layout Architecture
- **Layout Component** (`frontend/src/components/Layout.tsx`): Global wrapper used ONLY at App level
- **App.tsx** wraps entire Router with `<Layout>` - provides SearchBar, spacing, container
- **Individual pages** should NEVER import or use Layout directly - they're already inside it
- **Fixed SearchBar** requires `mt-[72px] pt-4` spacing: 72px margin clears SearchBar + 16px padding
- **Container**: `max-w-screen-2xl mx-auto px-4` provides consistent width and horizontal padding

### CRITICAL: Avoid Nested Layouts
Pages like AddProduct, AddStore should use React fragments (`<>`) not `<Layout>` to prevent:
- Duplicate main elements
- Inconsistent spacing
- Visual layout issues