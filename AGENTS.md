# AGENTS.md

This file provides general context and guidelines for AI agents and developers working on the `partle` project.

## 1. Project Overview

`partle` is a full-stack application with a Python FastAPI backend and a React frontend.

## 2. Setup Instructions

To get the project running locally:

*   **Backend:**
    *   Navigate to the `backend/` directory.
    *   Install dependencies: `poetry install`
    *   Run database migrations: `poetry run alembic upgrade head`
    *   Populate with mock data (if needed): `poetry run python stuff/populate_db.py`
    *   Start the server: `poetry run uvicorn app.main:app --reload`

*   **Frontend:**
    *   Navigate to the `frontend/` directory.
    *   Install dependencies: `npm install`
    *   Start the development server: `npm run dev`

## 3. Key Technologies

*   **Backend:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL
*   **Frontend:** React, Vite, Tailwind CSS, Vitest, Axios

## 4. Testing

*   **Backend:** `poetry run pytest` (from `backend/` directory)
*   **Frontend:** `npm test` (from `frontend/` directory)

## 5. Conventions & Guidelines

### Python (Backend)

*   **Code Style:** Use Ruff for linting and formatting. Prefer single quotes for strings. Numpydoc style for docstrings.
*   **Naming:** Adhere to standard Python naming conventions (e.g., `snake_case` for variables and functions, `PascalCase` for classes).
*   **Type Hinting:** Strongly prefer explicit type hints for all variables, function arguments, and return values, similar to TypeScript.

### General

*   **Commit Messages:** Start with a verb in the infinitive or imperative mood, with the first letter capitalized and the rest lowercase (e.g., "Fix: Resolve authentication bug", "Add: Implement new feature").
*   **Test-Driven Development (TDD):** Prefer a TDD approach. When solving problems or adding features, aim to write tests that capture the issue or new functionality, and ensure they pass.
*   Use trailing slashes in all API routes and fetch calls to avoid 307 redirects in FastAPI. Example: fetch(`${import.meta.env.VITE_API_BASE}/v1/health/`)