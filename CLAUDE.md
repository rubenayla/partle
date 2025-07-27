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
- Backend: pytest (check for test commands in pyproject.toml)
- Frontend: Vitest (configured in vite.config.js)