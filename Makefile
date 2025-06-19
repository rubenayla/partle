VENV_DIR=backend/.venv
PYTHON=$(shell pyenv which python)

.PHONY: setup test run

setup:
        cd backend && poetry config virtualenvs.in-project true
        cd backend && poetry env use $(PYTHON)
        cd backend && poetry install

test:
        cd backend && PYTHONPATH=. poetry run pytest tests

run:
        cd backend && poetry run uvicorn app.main:app --reload --port 8000
