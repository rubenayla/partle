# Partle
Search and find products near you, in any store.

Wallapop has commercial accounts now, with lots of expensive products littering the app because the stores are willing to pay premium subscriptions, because they actually need the visibility. Google Maps is trying (unsuccessfully) to integrate the products into the app too. I think the need is there, you can see it in these tangential apps trying to do it but not quite implementing it well.

For example, I want to search a product, sort by price and location, and find stores that are open now.

Yes, Amazon and AliExpress are taking a huge part of the market, but they are not ideal for super fast small purchases people often do on the go, to finish a task now, not tomorrow. Also, lots of stores are fed up of Amazon rules and want to sell their own way, with freedom. This market will never die. On top of that, there's a big push to buy and manufacture locally that will benefit this app.

## 🚀 Features
- 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
- 📍 View available stock in nearby stores
- 🗺 Toggle between list and map view
- ⚡ Quick sign-in with passkeys (fallback to email + password)

### Long term, not urgent
- What if i put the search terms at the left, the search bar at the top of the left section, and on startup the website already includes products as suggestions? The left search terms stay there, and the scroll only includes the products. The right is blank or left for ads etc.
- Mobile version (bottom to top, bar at the bottom with easy interface. Go ahead to new standards)
- Make map take the whole screen while keeping list with 4xl
Explore direct public key login (passkeys) so the browser handles authentication. If the key is lost, allow email-based reset.
- Do evaluation of each metric by the users, when
- Consider composite search mode with slide bars to select what I care more about, and instead of filter do a score assignation. For example, prioritize stock and distance over price when it's urgent, or prioritize price 
- Do AI search, consider external services or a language model that maps high level abstraction of the query with the closest product matches in the vector space.

## 🛠 Tech Stack

- Vite + React + Tailwind CSS
- Leaflet (OpenStreetMap) for map view
- FastAPI (planned) for backend API

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
│   ├── requirements.txt                # pip deps: fastapi, uvicorn, etc.
│   └── README.md                       # Backend usage notes
│
├── .gitignore
├── README.md                           # Top-level docs
└── dev.md                              # Dev notes, changelog, todos


## Introduction
Long term idea: When I want a strange M8 left-handed lock nut, some large metal zip tie or connector, having to go to 30 stores asking for the product is innefficient. Connect local business databases with the app so all products are listed there. Add AI thingy to load them to the database just by recording with the phone. It recognizes the products, screenshots them, lists the price, geo location and everything. You can go around stores and record to add thousands of products.
Add ratings.
Monetize with ads and premium positioning. Similar to wallapop (actually there are already businesses uploading stuff there). However, our idea is not to buy through the app, but just locate the products so they can be bought in person. It's for people who want to buy locally (super fast now), not online. For online shopping Aliexpress and Amazon are unbeatable.

Like Amazon, Aliexpress, Temu, Banggood, etc., but just lists products that are already available in local shops.

Let local businesses make an account, list the products, address, prices
Let people rate the business, products, and accuracy of the data (schedule)

levelsio uses gcloud Google Compute Engine

## 🛠 Dev Setup
Use the provided **Makefile** to set up the Python environment:

```bash
make setup
```

Run it from the repository root with no virtualenv active so it uses your
system Python. This creates `backend/.venv` and installs the backend in
editable mode along with `pytest` for running tests.

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
