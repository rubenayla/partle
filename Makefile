VENV_DIR=backend/.venv
PYTHON=$(shell which python3)

.PHONY: setup test run

setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -e backend

test:
	PYTHONPATH=backend $(VENV_DIR)/bin/pytest backend/tests

run:
	$(VENV_DIR)/bin/uvicorn app.main:app --reload --port 8000 --app-dir backend
