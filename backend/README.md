# Partle Backend

FastAPI backend serving local CSV data via `/api/search`.

---

## 🚀 Quickstart

### 0. System requirements

Ensure you have:

- Git
- Python 3.12.x (recommended via `pyenv`)
- SQLite (bundled)
- curl (optional, for testing)

---

## 🛠️ Setup Instructions (from scratch)

### 1. Install build tools (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y \
  build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncurses-dev libffi-dev liblzma-dev uuid-dev \
  libgdbm-dev tk-dev libnss3-dev libdb-dev libexpat1-dev \
  libxml2-dev libxmlsec1-dev libx11-dev libxext-dev libxrender-dev \
  xz-utils
```

---

### 2. Install pyenv (if not already installed)

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

Then install and activate Python 3.12.3:

```bash
pyenv install -s 3.12.3
pyenv global 3.12.3
```

---

### 3. Set up local Python & virtual environment

From inside the `backend/` folder:

```bash
cd backend
rm -rf .venv
poetry config virtualenvs.in-project true
poetry env use $(pyenv which python)
poetry install
```

Alternatively, from the project root you can run:

```bash
make setup
```
Run this from the repository root without an active virtualenv so it uses your
pyenv Python.

---

### 4. Install backend project + dependencies

Dependencies are installed via Poetry in the previous step. You can also run
`make setup` from the repository root to perform the same actions.

---

## Create the database tables

To create the database tables, run the Alembic migrations from the `backend` directory:

```bash
poetry run alembic upgrade head
```

For more detailed instructions on setting up the database, please see the main [README.md](../../README.md#database-setup).

## ▶️ Run the development server

```bash
uvicorn app.main:app --reload --port 8000
```

- http://localhost:8000/docs – interactive API
    - http://localhost:8000/docs#/Parts/add_part_v1_parts_post
- http://localhost:8000/v1/parts – get all parts

Then open:  
[http://localhost:8000/api/search?q=JST](http://localhost:8000/api/search?q=JST)

---

### 🧪 Quick test

Alternatively run the server via the Makefile:

```bash
make run
```

Then visit:

- <http://localhost:8000/> → `{"status":"ok","version":"v1","docs":"/docs"}`
- <http://localhost:8000/docs> → Swagger UI
- <http://localhost:8000/v1/parts> → should return `404` if the router is empty (or list your endpoints)

## 📂 Directory structure

```
backend/
├── pyproject.toml             ← modern build config (PEP 621)
├── README.md                  ← this file
├── app/
│   ├── main.py                ← FastAPI app instance
│   ├── api.py                 ← `/api/search` endpoint
│   ├── models.py              ← Pydantic schema
│   ├── db.py                  ← CSV loader
│   └── store_data.csv         ← mock dataset
```

---

## 🧪 Test from terminal

```bash
curl "http://localhost:8000/api/search?q=connector"
```

