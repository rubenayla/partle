# Partle Backend

FastAPI backend serving local data.

## Quickstart

1. From the repository root, create the virtual environment and install dependencies:

```bash
make setup
```

2. Activate the environment (optional):

```bash
source backend/.venv/bin/activate
```

3. Start the server:

```bash
make run
```

The API will be available at `http://localhost:8000`.

## Testing

```bash
make test
```

## Database setup

Run once to create the SQLite tables:

```bash
python -m app.db.base
```

## Directory structure

```
backend/
├── app/
│   ├── api/
│   ├── db/
│   ├── schemas/
│   └── main.py
├── tests/
└── pyproject.toml
```
