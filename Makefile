# ───────────────────────────────
#  Partle – project-root Makefile
# ───────────────────────────────
# Tabs are required at the start of every recipe line.

BACKEND_DIR  := backend
FRONTEND_DIR := frontend           # adjust if the React folder is elsewhere
PY           := poetry run
UVICORN_CMD  := $(PY) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Default DSN; override on the CLI:  make dev DATABASE_URL=postgresql://…
export DATABASE_URL ?= postgresql://postgres:partl3p4ss@localhost:5432/partle

# -------- help ------------------------------------------------------------
.PHONY: help
help:  ## list targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "\033[36m%-12s\033[0m %s\n",$$1,$$2}'

# -------- dependencies ----------------------------------------------------
.PHONY: install
install:
	@echo "Setting up backend environment..."
	@if ! command -v python3 >/dev/null; then \
		echo "Python 3 is required but not found."; exit 1; \
	fi
	@python3 -m venv backend/.venv
	@backend/.venv/bin/pip install -U pip
	@backend/.venv/bin/pip install poetry
	@cd backend && ../backend/.venv/bin/poetry lock
	@cd backend && ../backend/.venv/bin/poetry install

# -------- database & migrations ------------------------------------------
.PHONY: db-init
db-init:            ## create DB if missing + run migrations
	@createdb --if-not-exists partle 2>/dev/null || true
	@(cd backend && DATABASE_URL=$(DATABASE_URL) poetry run alembic upgrade head)


.PHONY: migrate
migrate: NAME=                  ## make migrate NAME=add_price_column
migrate:
	@if [ -z "$(NAME)" ]; then echo "✖ NAME=<slug> missing"; exit 1; fi
	@(cd $(BACKEND_DIR) && DATABASE_URL=$(DATABASE_URL) \
	  $(PY) alembic revision --autogenerate -m "$(NAME)")
	$(MAKE) db-init

# -------- run servers -----------------------------------------------------
.PHONY: backend
backend: db-init                 ## start FastAPI only
	@(cd $(BACKEND_DIR) && DATABASE_URL=$(DATABASE_URL) $(UVICORN_CMD))

.PHONY: frontend
frontend:                        ## start Vite dev server only
	@[ -d $(FRONTEND_DIR) ] && npm --prefix $(FRONTEND_DIR) run dev \
	  || echo "⚠  $(FRONTEND_DIR) not found"

.PHONY: dev
dev: db-init                     ## backend + frontend (Ctrl-C twice to quit)
	@(cd $(BACKEND_DIR) && DATABASE_URL=$(DATABASE_URL) $(UVICORN_CMD)) & \
	 npm --prefix $(FRONTEND_DIR) run dev

# -------- tests -----------------------------------------------------------
.PHONY: test
test:                            ## run pytest
	@(cd $(BACKEND_DIR) && $(PY) pytest -q)
