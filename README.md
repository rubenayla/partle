# Partle

Search and find electronic/hardware parts near you. Fast. Local. Stock-based.

## 🚀 Features

- 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
- 📍 View available stock in nearby stores
- 🗺 Toggle between list and map view
- ⚡ No login, no fluff—just results

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

### 1. Install Node.js (Ubuntu)

Recommended: use **nvm** for easier upgrades.

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Load nvm into shell
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

# Install and use latest LTS version of Node.js
nvm install --lts
nvm use --lts
```

---

### 2. Create and run the frontend app

From the project root (`partle/`):

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

---

### 3. Install Tailwind CSS (stable version)

> ⚠️ Use **Tailwind CSS v3** for compatibility with tooling

```bash
npm install -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

This creates:
- `tailwind.config.js`
- `postcss.config.js`

Then edit `tailwind.config.js`:

```js
content: [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
],
```

And in `src/index.css`, add:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

### 4. Start the app

```bash
npm run dev
```

Then visit `http://localhost:5173` in your browser.


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
    - 