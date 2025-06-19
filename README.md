# Partle
Search and find products near you, in any store.
For stores, show any product you have in stock to get more sales.

When I want a strange M8 left-handed lock nut, instead of having to drive to 30 stores, 20 of which are closed, to maybe get 1 that might have it at super expensive price after spending all day, I search in Partle, sort by price and distance, and go to the store that is open and has in stock.

Yes, it looks like the kind of thing Google would do, but it doesn't exist. Google Maps has products and stores and might end up working in the future, but it doesn't work now. You won't find the products you're looking for. Just try.

Wallapop has commercial accounts now, with lots of new expensive products littering the app because the stores are willing to pay premium subscriptions, because they actually need the visibility. You can see the need is there, in these tangential apps trying to do it but not quite implementing it well.

Yes, Amazon and AliExpress are taking a huge part of the market, but they are not so fast as you going yourself, not as good as being able to see the product before you buy it, and they come with inner politics that bother lots of businesses. Lots of stores are fed up of Amazon rules and want to sell their own way, with freedom. About AliExpress, there's a powerful push to manufacture locally, not depend on one country to make everything in the world.

Monetize with ads and premium positioning, like wallapop.

In the long term:
- connect local business databases with the app so all products are listed there.
- Leverage AI to search with natural language, human-like queries and descriptions, images etc.
- Let user find cool things close by, knowing what they like in depth. Notification when passing by a liked product.

## 🚀 Features
- 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
- 📍 View available stock in nearby stores
- 🗺 Toggle between list and map view
- ⚡ Quick sign-in with passkeys (fallback to email + password)

## 🛠 Tech Stack
- **frontend/** uses Node.js, Vite + React + Tailwind CSS, and Leaflet (OpenStreetMap) for map view
    - Manages dependencies with npm. No Python virtual environment is needed.
- **backend/**
    - uses pyenv Python, so i can pick versions easily with no /usr/bin/python mess
    - Poetry to manage dependencies in one tool, possibly combine with uv for fast installation. Should be compatible, and it's not a dependency per se.
    - FastAPI
    - PostgreSQL, SQLAlchemy ORM to access it, and Alembic to manage migrations
    - Running `make setup` creates `backend/.venv` and installs dependencies there.

Keeping these environments independent prevents dependency conflicts, keeps tooling isolated, and simplifies debugging. Stick with this layout—it is industry standard.

## 📦 Project Structure
partle/
├── frontend/                           # React + Vite + Tailwind + Leaflet
│   ├── public/                         # Static assets (e.g. icons)
│   └── src/
│       ├── assets/                     # Images, logos, etc.
│       ├── components/                 # Reusable components (e.g. Header, Card)
│       ├── pages/                      # Views (ListView, MapView)
│       ├── data/                       # (temp) mock inventory JSON
│       ├── App.jsx                     # Main app logic (routing, layout)
│       ├── main.jsx                    # React entry point
│       └── index.css                   # Tailwind CSS entrypoint
│
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/                            # FastAPI backend
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint (uvicorn)
│   │   ├── api.py                      # /search, /stores endpoints
│   │   ├── models.py                   # Pydantic schemas: Part, Store, Query
│   │   ├── db.py                       # Data loader (CSV → memory or DB)
│   │   └── store_data.csv              # CSV inventory store (for now)
│   ├── pyproject.toml                  # Poetry config
│   ├── poetry.lock                     # Locked dependencies
│   └── README.md                       # Backend usage notes
│
├── .gitignore
├── README.md                           # Top-level docs
└── dev.md                              # Dev notes, changelog, todos

## 🛠 Dev Setup
Use the provided **Makefile** to set up the Python environment (via Poetry):

```bash
make setup
```

Run it from the repository root with no virtualenv active so it uses your
pyenv-managed Python. This creates `backend/.venv` with Poetry and installs
all dependencies.

### 1. Install Node.js
Make sure Node.js 18+ is available. The `nvm` tool is recommended but not
required.

### 2. Prepare the frontend

From the project root run:

```bash
cd frontend
npm install
```

Tailwind CSS is already configured (see `tailwind.config.js`).

### 3. Start the backend API

From the `backend/` folder start the FastAPI server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

You can also start it with Makefile:

```bash
make run
```

### 4. Start the frontend app

From the `backend/` folder start the FastAPI server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

You can also start it with Makefile:

```bash
make run
```

### 5. Start the frontend app

Run the Vite dev server from inside the `frontend/` folder:

```bash
cd ../frontend
npm run dev
```

Then visit `http://localhost:5173` in your browser. **Important:** use
`localhost` in the URL (not `127.0.0.1`) so it matches the CORS rule configured
in `backend/app/main.py`.


## References
- Recommended apps for prototype:
    - Pop app
    - Marvel app
    - Sketch
    - Figma
    - Invision
- Recommended apps for MVP:
    - Wix
    - Launch Rocks
    - Wordpress
    - Weebly
    - Site123
    - Gofundme
    - Google AdWords
    - Facebook Business Manager
    - Stripe
    - Mailchimp

## 🧪 Running tests

Unit tests live under `backend/tests/` and use **pytest**. To run them:

```bash
PYTHONPATH=backend pytest backend/tests
```

Or simply run:

```bash
make test
```
