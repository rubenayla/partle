# Partle

Search and find products near you, in any store.
For stores, show any product you have in stock to get more sales.

When I want a strange M8 left-handed lock nut, instead of having to drive to 30 stores, 20 of which are closed, to maybe get 1 that might have it at super expensive price after spending all day, I search in Partle, sort by price and distance, and go to the store that is open and has in stock.

Yes, it looks like the kind of thing Google would do, but it doesn't exist. Google Maps has products and stores and might end up working in the future, but it doesn't work now. You won't find the products you're looking for. Just try.

Wallapop has commercial accounts now, with lots of new expensive products littering the app because the stores are willing to pay premium subscriptions, because they actually need the visibility. You can see the need is there, in these tangential apps trying to do it but not quite implementing it well.

Yes, Amazon and AliExpress are taking a huge part of the market, but they are not so fast as you going yourself, not as good as being able to see the product before you buy it, and they come with inner politics that bother lots of businesses. Lots of stores are fed up of Amazon rules and want to sell their own way, with freedom. About AliExpress, there's a powerful push to manufacture locally, not depend on one country to make everything in the world.

Monetize with ads and premium positioning, like wallapop.

In the long term:

* connect local business databases with the app so all products are listed there.
* Leverage AI to search with natural language, human-like queries and descriptions, images etc.
* Let user find cool things close by, knowing what they like in depth. Notification when passing by a liked product.

## 🚀 Features

* 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
* 📍 View available stock in nearby stores
* 🗺 Toggle between list and map view
* ⚡ Quick sign-in with passkeys (fallback to email + password)

## 🛠 Tech Stack

* **frontend/** uses Node.js, Vite + React + Tailwind CSS, and Leaflet (OpenStreetMap) for map view

  * Manages dependencies with npm. No Python virtual environment is needed.
* **backend/**

  * uses pyenv Python, so i can pick versions easily with no /usr/bin/python mess
  * Poetry to manage dependencies in one tool, possibly combine with uv for fast installation. Should be compatible, and it's not a dependency per se.
  * FastAPI
  * PostgreSQL, SQLAlchemy ORM to access it, and Alembic to manage migrations
  * Running `make setup` creates `backend/.venv` and installs dependencies there.

Keeping these environments independent prevents dependency conflicts, keeps tooling isolated, and simplifies debugging. Stick with this layout—it is industry standard.

## 📦 Project Structure

```
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
│   │   ├── api/
│   │   │   └── v1/                     # Versioned routes
│   │   │       ├── auth.py
│   │   │       ├── parts.py
│   │   │       └── stores.py
│   │   ├── auth/                       # Auth helpers
│   │   │   └── utils.py
│   │   ├── db/                         # SQLAlchemy setup
│   │   │   ├── base.py
│   │   │   ├── base_class.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── schemas/                    # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── part.py
│   │   │   └── store.py
│   │   └── main.py                     # FastAPI entrypoint
│   ├── alembic/                        # Database migrations
│   ├── alembic.ini
│   ├── partle.db                       # SQLite dev database
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_fast_api.py
│   ├── pyproject.toml                  # Poetry config
│   ├── poetry.lock                     # Locked dependencies
│   └── README.md                       # Backend usage notes
│
├── .gitignore
├── README.md                           # Top-level docs
├── AGENTS.md
├── Makefile
├── TODO.md
├── dev_setup.sh
└── package-lock.json
```

## Development setup

### 🚀 Quick start (new machine)

```bash
# 1. Clone repo
git clone https://github.com/<your-github-org>/partle.git && cd partle   # replace <your-github-org> with your GitHub org or username

# 2. First‑time install (backend deps via Poetry, frontend deps via npm)
make install

# 3. Launch everything (creates DB, runs migrations, starts API & React)
make dev
```

The backend expects `DATABASE_URL` to default to
`postgresql://postgres:partl3p4ss@localhost:5432/partle`.
If you use a different user / password / host:

```bash
make dev DATABASE_URL=postgresql://myuser:mypw@dbhost:5432/partle
```

---

### Manual steps (optional)

If you prefer to run things separately:

```bash
# backend only (ensures DB + migrations)
make backend

# frontend only
make frontend
```

---

## References

* Prototype tools: PopApp, Marvel, Sketch, Figma, Invision
* MVP helpers: Wix, LaunchRocks, WordPress, Site123, Stripe, Mailchimp, etc.

## 🧪 Running tests

```bash
PYTHONPATH=backend pytest backend/tests
# or simply
make test
```
