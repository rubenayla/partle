.PHONY: setup install test run shell migrate upgrade clean

# Create system + project environment
setup:
	./dev_setup.sh

# Just install Python dependencies
install:
	cd backend && poetry install

# Run tests
test:
	cd backend && poetry run pytest backend/tests

# Run the dev server
run:
	cd backend && poetry run uvicorn app.main:app --reload --port 8000 --app-dir backend

# Drop into poetry shell
shell:
	cd backend && poetry shell

# Alembic commands
migrate:
	cd backend && poetry run alembic revision --autogenerate -m "auto"

upgrade:
	cd backend && poetry run alembic upgrade head

# Clean venv and build artifacts
clean:
	rm -rf backend/.venv __pycache__ **/__pycache__ .mypy_cache
