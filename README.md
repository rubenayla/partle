# Partle

Search and find products near you, in any store.
For stores, show any product you have in stock to get more sales.

When I want a strange M8 left-handed lock nut, instead of having to drive to 30 stores, 20 of which are closed, to maybe get 1 that might have it at super expensive price after spending all day, I search in Partle, sort by price and distance, and go to the store that is open and has in stock.

Yes, it looks like the kind of thing Google would do, but it doesn't exist. Google Maps has products and stores and might end up working in the future, but it doesn't work now. You won't find the products you're looking for. Just try.

Wallapop has commercial accounts now, with lots of new expensive products littering the app because the stores are willing to pay premium subscriptions, because they actually need the visibility. You can see the need is there, in these tangential apps trying to do it but not quite implementing it well.

Yes, Amazon and AliExpress are taking a huge part of the market, but they are not so fast as you going yourself, not as good as being able to see the product before you buy it, and they come with inner politics that bother lots of businesses. Lots of stores are fed up of Amazon rules and want to sell their own way, with freedom. About AliExpress, there's a powerful push to manufacture locally, not depend on one country to make everything in the world.

Monetize with ads and premium positioning, like wallapop.

In the long term:

* Connect local business databases with the app so all products are listed there.
* Leverage AI to search with natural language, human-like queries and descriptions, images etc.
* Let user find cool things close by, knowing what they like in depth. Notification when passing by a liked product.

## Design ideas
A product should belong to a store, and a store can be controlled by several users. All users that belong to a store can add remove or modify products linked to that store oficially. Usera can also add products to other stores, but the products will be unofficial, will have a different tag. If a store owner accepts it, it will become official.

To let a product data be managed automatically, the store will be able to connect the database with stock amounts prices etc, to the app via an API.

Users can rate the reliability of almost all data shown about products and stores. Similar to community notes in x, giving unreliable rating will make you lose reliability rating as a user yourself. Somehow the UI could reflect this reliability rating and include it in the search algorithm, or let it be replaced by an unofficial product if the rating difference is big enough (should include rating number too). Consider users spamming products, what effect do they have.

## 🚀 Features

* 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
* 📍 View available stock in nearby stores
* 🟘 Toggle between list and map view
* ⚡ Quick sign-in with passkeys (fallback to email + password)

## 📦 Tech Stack

- **frontend/** uses Node.js, Vite + React + Tailwind CSS, and Leaflet (OpenStreetMap) for map view
    - Manages dependencies with npm. No Python virtual environment is needed.
    - I prefer TypeScript for type safety
- **backend/**
    - Uses `pyenv` to manage Python versions
    - Poetry for Python dependency management, optionally combined with `uv` for fast installation
    - FastAPI as backend server
    - PostgreSQL with SQLAlchemy ORM and Alembic for migrations
    - Running `make setup` creates `backend/.venv` and installs dependencies
    - Fido2

This separation avoids dependency conflicts and is standard practice.

## 🚀 Install (new machine)

### Install Python (better with pyenv) in the root folder, partle/, for both the frontend and backend.

If you don't have Python 3.12+ available, or want to avoid system Python conflicts, use [pyenv](https://github.com/pyenv/pyenv):

```bash
# Install pyenv (Debian/Ubuntu example)
curl https://pyenv.run | bash
# Add pyenv to PATH (follow instructions after install)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# Install Python 3.12
pyenv install 3.12.3
# Set it as the local Python for this repo
cd ~/repos/partle
pyenv local 3.12.3
```

---

1. **Clone the repo:**

   ```bash
   git clone https://github.com/<your-github-org>/partle.git && cd partle
   ```
2. **(Alternative) Install Python 3.12+ via system package manager:**

   ```bash
   sudo apt install python3.12 python3.12-venv python3.12-dev
   ```
3. **Set up environment variable for frontend to reach backend:**

   ```bash
   echo "VITE_API_BASE=http://localhost:8000" > frontend/.env
   ```
4. **Install all backend/frontend dependencies:**

   ```bash
   make install
   ```

   *Sets up venv, Poetry, npm packages, etc.*

> **Requires Python 3.12 or newer.**
> If missing, see install tips above or in [#Development](#development).

**Default backend DB URL:**

```
postgresql://postgres:partl3p4ss@localhost:5432/partle
```

*To override (e.g. use a custom DB):*

```
make dev DATABASE_URL=postgresql://user:pw@host:port/db
```

---

## 🏃‍♂️ Run the app

* **Start both frontend and backend (dev mode):**

  make dev

* **Or run separately:**

  make backend    # starts FastAPI backend on :8000
  make frontend   # starts Vite/React frontend on :5173

* **Directly:**

  * Frontend: npm run dev --prefix frontend
  * Backend:  poetry run uvicorn app.main\:app --reload --host 0.0.0.0 --port 8000 --log-level debug

---

## 🌍 Deployed Setup

* **Frontend (React):** hosted on [Vercel](https://vercel.com/)
  Live: [https://partle.vercel.app](https://partle.vercel.app)
* **Backend (FastAPI):** hosted on [Railway](https://railway.app/)
  Public API base: [https://partle-production.up.railway.app](https://partle-production.up.railway.app)

Frontend uses `import.meta.env.VITE_API_BASE` to locate the backend.
This must be:

* Set in `frontend/.env` locally for dev (`VITE_API_BASE=http://localhost:8000`)
* Set in Vercel project settings for prod (`VITE_API_BASE=https://...`)

---

### Local URLs

* **Frontend:** [http://localhost:5173/](http://localhost:5173/)
* **Backend:**

  * [http://localhost:8000/docs](http://localhost:8000/docs)    (API docs)
  * [http://localhost:8000/redoc](http://localhost:8000/redoc)   (ReDoc docs)
  * [http://localhost:8000/v1/parts](http://localhost:8000/v1/parts)  (API endpoint)
  * [http://localhost:8000/v1/stores](http://localhost:8000/v1/stores) (API endpoint)
  * [http://localhost:8000/docs#/Auth/register\_auth\_register\_post](http://localhost:8000/docs#/Auth/register_auth_register_post)

## 📆 Project Structure

```bash
partle/
├── frontend/
│   ├── public/                         # Static assets
│   └── src/
│       ├── assets/                    # Logos, icons, etc
│       ├── components/                # Reusable UI components
│       ├── pages/                     # Views (Home, Stores, Products, etc.)
│       ├── data/                      # Temp: mock JSON data
│       ├── App.tsx                    # Main routing
│       ├── main.tsx                   # React root
│       └── index.css                  # Tailwind entrypoint
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/v1/                    # Routes
│   │   │   ├── auth.py
│   │   │   ├── parts.py
│   │   │   └── stores.py
│   │   ├── auth/utils.py              # Auth logic
│   │   ├── db/                        # DB engine
│   │   │   ├── base.py
│   │   │   ├── base_class.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── part.py
│   │   │   └── store.py
│   │   └── main.py                    # FastAPI entrypoint
│   ├── alembic/                       # Migrations
│   ├── alembic.ini
│   ├── partle.db                      # SQLite (dev only)
│   ├── tests/                         # Backend tests
│   │   ├── test_api.py
│   │   └── test_fast_api.py
│   ├── pyproject.toml                 # Poetry config
│   ├── poetry.lock
│   └── README.md                      # Backend usage
├── Makefile
├── dev_setup.sh
├── README.md                          # (this file)
├── .gitignore
├── package-lock.json
├── AGENTS.md
└── TODO.md
```

## 🔮 References

- UI prototyping: Figma, Sketch, PopApp, Invision
- MVP tooling: Wix, Stripe, Mailchimp, WordPress, Site123

## 🤕 Tests

```bash
# backend tests
make test
# or directly
PYTHONPATH=backend pytest backend/tests
```
