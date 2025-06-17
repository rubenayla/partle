# Partle
Search and find products near you, in any store.

Wallapop has commercial accounts now, with lots of expensive products littering the app because the stores are willing to pay premium subscriptions, because they actually need the visibility. Google Maps is trying (unsuccessfully) to integrate the products into the app too. I think the need is there, you can see it in these tangential apps trying to do it but not quite implementing it well.

Yes, Amazon and AliExpress are taking a huge part of the market, but they are not ideal for super fast small purchases people often do on the go, to finish a task now, not tomorrow. Also, lots of stores are fed up of Amazon rules and want to sell their own way, with freedom. This market will never die.

## 🚀 Features
- 🔍 Search by part name or spec (e.g. "JST 6-pin", "M8 locking nut")
- 📍 View available stock in nearby stores
- 🗺 Toggle between list and map view
- ⚡ No login, no fluff—just results

## To-Do
- Hosting partle.rubenayla.xyz
- Backend
- Add Accounts
    > Required mainly just to upload products. Also rate them, save favourites, skip ads with paid tiers etc.
    - Up to down, "You'll probably like the passkey method, since you won't need to enter passwords or use your phone. The browser will remember the keys and it will be safer". passkeys/WebAuthn in the FIDO2 standard
    - Otherwise, here's you can register/login it with email and password (Just enter your details. If an account exists, it will log you in, otherwise it will create a new one)
- add modification date to db and system
- Add API so clients can add products (and stores?)
- Add UI to add stores
- Add UI to add products
- Tune the reliability rating of the info uploaded. It should go -1 to 1. Start at 0, depending on other people ratings get modified.
- Get data
    - Scraping?
        - Google Maps
        - Amazon
        - Wallapop?
    - Ask gpt sources
- The product of each store must have a unique name. If you don't agree with the data, several versions will appear, with capability to up/down vote them. It just like several products squished together in the same frontend card.
- Mechanism to store searches performed by users so we can know what products are demanded

### Long term, not urgent
- Mobile version (bottom to top, bar at the bottom with easy interface. Go ahead to new standards)
- Make map take the whole screen while keeping list with 4xl
Can I use that public key login method i thought of? Just add your public key when logging in and let your browser authenticate you, just like websites authenticate themselves with ssl certificates. However if the private key is lost, it should be reset with email or something, like normal passwords. However the key is safer and easier to use (automatic)


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

Run the frontend development server from inside the `frontend/` folder:

```bash
cd frontend
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

## 🧪 Running tests

Unit tests live under `backend/tests/` and use **pytest**. To run them:

```bash
PYTHONPATH=backend pytest backend/tests
```
