# Backend Makefile - Simple commands for development and deployment

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make migrate        - Run database migrations"
	@echo "  make migration MSG  - Create a new migration"
	@echo "  make server         - Start development server"
	@echo "  make test          - Run tests"
	@echo "  make backup        - Create database backup"

.PHONY: migrate
migrate:
	@echo "⚠️  To run migrations safely, use: ./scripts/migrate.sh"
	@echo "Or if you're sure: export \$$(grep DATABASE_URL .env) && uv run alembic upgrade head"

.PHONY: migration
migration:
	@test -n "$(MSG)" || (echo "Usage: make migration MSG='your message'" && exit 1)
	uv run alembic revision -m "$(MSG)"

.PHONY: server
server:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: test
test:
	uv run pytest

.PHONY: backup
backup:
	@echo "Creating backup..."
	@mkdir -p backups
	@uv run python -c "from app.core.config import settings; import subprocess; subprocess.run(['pg_dump', settings.DATABASE_URL, '-f', f'backups/backup_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.sql'])"
	@echo "Backup created in backups/"