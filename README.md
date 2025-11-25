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

### Adding Products

Products can be added via the frontend UI or directly through the backend API.

**Via UI:**
1. Ensure both frontend and backend are running (`make dev`).
2. Navigate to the "Add Product" page in the frontend (usually accessible via a link in the UI).
3. Fill out the form with product details (name, spec, price, etc.) and select a store if applicable.
4. Click "Save" to add the product.

**Via API:**
Products can be added by sending a `POST` request to the `/v1/products` endpoint of the backend API.

**Endpoint:** `POST /v1/products`
**Base URL (local dev):** `http://localhost:8000`

**Request Body (JSON):**
```json
{
  "name": "Example Product Name",
  "store_id": 1,
  "spec": "Product Specification",
  "price": 19.99,
  "url": "http://example.com/product",
  "lat": 34.052235,
  "lon": -118.243683,
  "description": "A detailed description of the product."
}
```
**Authentication:** Requires a valid JWT in the `Authorization: Bearer <token>` header.

For more details on the API schema, refer to `backend/app/schemas/product.py` and `backend/app/api/v1/products.py`.

## 🤖 AI and API Discoverability

To optimize the site for AI search and allow AI agents to discover and potentially use the API, the following files and configurations have been implemented:

*   **`robots.txt`**: Located at `frontend/public/robots.txt`, this file provides instructions to web crawlers, including AI bots like `GPTBot` and `Google-Extended`, on which parts of the site they are allowed or disallowed to access. It is configured to allow full access and points to the `sitemap.xml`.

*   **`ai.txt`**: Located at `frontend/public/ai.txt`, this emerging standard file provides specific instructions and usage rights for AI crawlers and models, indicating that the site's content can be used for training purposes.

*   **`openapi.json`**: Generated from the FastAPI backend and located at `frontend/public/api/openapi.json`, this file provides a machine-readable description of the entire backend API. It details available endpoints, their parameters, and expected responses, enabling AI agents to understand and interact with the API programmatically.

*   **`sitemap.xml`**: Located at `frontend/public/sitemap.xml`, this file lists all the public pages of the website, helping crawlers efficiently discover and index all content.

*   **Structured Data (Schema.org)**: Implemented on product detail pages (`frontend/src/pages/ProductDetail.jsx`), this uses JSON-LD to embed rich, semantic information about products directly into the HTML. This allows AI models to unambiguously understand product attributes like name, price, description, and availability, enhancing discoverability and enabling richer search results.
    *   The `react-helmet-async` library has been added to the frontend (`frontend/package.json` and `frontend/src/main.tsx`) to facilitate injecting this structured data into the document's `<head>`.

## 📦 Tech Stack

- **frontend/** uses Node.js, Vite + React + Tailwind CSS, Radix UI for accessible components, and Leaflet (OpenStreetMap) for map view
    - Manages dependencies with npm. No Python virtual environment is needed.
    - I prefer TypeScript for type safety
- **backend/**
    - Uses `pyenv` to manage Python versions
    - UV for Python dependency management
    - FastAPI as backend server
    - PostgreSQL with SQLAlchemy ORM and Alembic for migrations
    - Running `make setup` creates `backend/.venv` and installs dependencies
    - Fido2

This separation avoids dependency conflicts and is standard practice.

## 🚀 Install (new machine)

### 1. Set up SSH Key for GitHub

To clone the repository using SSH, you'll need to add an SSH key to your GitHub account.

First, check for existing SSH keys:

```bash
ls -al ~/.ssh
```

If you see `id_ed25519.pub` or `id_rsa.pub`, you already have a key and can skip to the next step.

If not, create a new SSH key:

```bash
# Create a new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com, or something to identify the key"

# Start the ssh-agent in the background
eval "$(ssh-agent -s)"

# Add your SSH private key to the ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy the SSH public key to your clipboard
cat ~/.ssh/id_ed25519.pub
```

Next, add the copied public key to your GitHub account. Follow the instructions here:
[https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

Finally, verify your connection:
```bash
ssh -T git@github.com
```

### 2. Clone the repo

```bash
git clone git@github.com:rubenayla/partle.git && cd partle
```

### 3. Quick Setup (Recommended)

For a quick and automated setup, run the `dev_setup.sh` script:

```bash
./dev_setup.sh
```

This script will install system dependencies, Node.js via nvm, set up the frontend, and configure the Python backend with pyenv and UV.

### 4. Manual Setup (Alternative)

If you prefer a step-by-step manual installation, follow these instructions:

#### 4.1. Set up Python 3.12+

If you don't have Python 3.12+ available, or want to avoid system Python conflicts, use [pyenv](https://github.com/pyenv/pyenv):

```bash
# Install pyenv (Debian/Ubuntu example)
curl https://pyenv.run | bash
# Add pyenv to PATH (follow instructions after install)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# Install Python 3.12 and set it as the local version
pyenv install 3.12.3
pyenv local 3.12.3
```

**(Alternative) Install Python 3.12+ via system package manager:**

```bash
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### 4.2. Set up environment variable for frontend to reach backend

```bash
echo "VITE_API_BASE=http://localhost:8000" > frontend/.env
```

#### 4.3. Install all backend/frontend dependencies

```bash
make install
```

   *Sets up venv, UV, npm packages, etc.*

   **Note on Frontend Dependencies:** Due to potential peer dependency conflicts with React 19 and some libraries (e.g., `@testing-library/react`, `react-leaflet`), `npm install` might require the `--force` flag to resolve. While generally not recommended for production, this can be used in development to proceed with installation:
   ```bash
   npm install --force
   ```

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
  make frontend   # starts Vite/React frontend on :3000

* **Directly:**

  * Backend:  uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
  * Frontend: npm run dev --prefix frontend -- --port 3000

---

## 💾 Database Setup

This project uses PostgreSQL as its primary database. For a simpler, file-based setup, you can use SQLite.

### PostgreSQL (Recommended)

1.  **Install PostgreSQL:**

    If you haven't already, install PostgreSQL on your system. On Debian/Ubuntu, you can use:

    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```

2.  **Create the database and user:**

    You'll need to create a database and a user for the application. You can do this by running the following commands in your terminal:

    ```bash
    sudo -u postgres psql -c "CREATE USER partle WITH PASSWORD 'partl3p4ss'"
    sudo -u postgres psql -c "CREATE DATABASE partle OWNER partle"
    ```

    You can replace `partle` and `partl3p4ss` with your desired database name, username, and password.

3.  **Set the `DATABASE_URL` environment variable:**

    The application uses the `DATABASE_URL` environment variable to connect to the database. The default is `postgresql://postgres:partl3p4ss@localhost:5432/partle`. If you used different credentials, you'll need to set this variable.

    You can set it in a `.env` file in the `backend` directory, or by exporting it in your terminal:

    ```bash
    export DATABASE_URL="postgresql://user:pw@host:port/db"
    ```

4.  **Run the database migrations:**

    Once the database is created and the `DATABASE_URL` is set, you can run the database migrations:

    ```bash
    cd backend
    uv run alembic upgrade head
    ```

### SQLite (for simple local development)

If you prefer to use SQLite, you can set the `DATABASE_URL` to point to a local file:

```bash
export DATABASE_URL="sqlite:///partle.db"
```

The database file will be created in the `backend` directory. You'll still need to run the migrations as described above.

---

## 🌍 Deployed Setup

* **Frontend (React):** hosted on Hetzner server
* **Backend (FastAPI):** deployment TBD
  Public API base: TBD

Frontend uses `import.meta.env.VITE_API_BASE` to locate the backend.
This must be:

* Set in `frontend/.env` locally for dev (`VITE_API_BASE=http://localhost:8000`)
* Set in production environment for prod (`VITE_API_BASE=https://...`)

## 🖥️ Server Quick Reference

### Public access
- **Website:** https://partle.rubenayla.xyz
- **API docs:** https://partle.rubenayla.xyz/docs

### Port map

| Service | Port | Scope |
|---------|------|-------|
| Frontend (React) | 3000 | Internal/dev |
| Backend (FastAPI) | 8000 | Internal/dev |
| PostgreSQL | 5432 | Internal |
| Elasticsearch | 9200 | Internal |
| Nginx HTTP | 80 | Public |
| Nginx HTTPS | 443 | Public |

### Local development ports

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Frontend (Vite) | 3000 | http://localhost:3000 | React dev server |
| Backend (FastAPI) | 8000 | http://localhost:8000 | API server |
| PostgreSQL | 5432 | localhost | App database |
| Elasticsearch | 9200 | http://localhost:9200 | Search engine |

### Operational shortcuts

```bash
# Start backend on server
sudo /srv/partle/start-backend.sh

# Start frontend on server
sudo /srv/partle/start-frontend.sh

# Check both processes
ps aux | grep -E "(uvicorn|vite)"

# Local dev servers
cd frontend && npm run dev -- --port 3000
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Key server paths
- `/srv/partle/backend/.env` – backend secrets/config
- `/srv/partle/frontend/.env` – frontend runtime config
- `/etc/nginx/sites-available/partle.rubenayla.xyz` – reverse proxy config
- Detailed deployment/ops steps → `docs/deployment.md`

### Database snapshot
- **Connection:** `postgresql://partle_user:partle_secure_password@localhost:5432/partle`
- **Products:** ~37 items
- **Users:** ~12 accounts
- **Stores:** ~4,000 locations

### Internal services
- **Frontend dev server:** on :3000 (Vite) and proxied by Nginx for `/`
- **Backend API:** on :8000 (FastAPI) and proxied to `/api`, `/docs`, `/health`
- **PostgreSQL:** on :5432 (backend only)
- **Elasticsearch:** on :9200 (backend only)

### Service checks & firewall
```bash
# Inspect listeners
sudo netstat -tlnp | grep -E "(3000|8000|5432|9200|80|443)"

# Restart key services
sudo systemctl restart nginx postgresql elasticsearch

# Firewall helpers
sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw deny 3000/tcp 8000/tcp 5432/tcp 9200/tcp
```

### Common issues & quick fixes
- **Frontend shows “Network Error”** – Backend likely isn’t running or `VITE_API_BASE` points to the wrong host; restart FastAPI on port 8000.
- **Emails not sending** – Check that the Resend DNS records have propagated and that the `RESEND_API_KEY` secret exists in the Cloudflare Worker.
- **GitHub Actions fail because `uv` isn’t found** – Add `/home/deploy/.local/bin` to the PATH for the runner or deployment user.
- **Need mock/test data** – By default `/v1/products/` hides items tagged `mock-data`; append `?include_test_data=true` to include them.

## 📚 MkDocs documentation site
- Source files live in `/docs`; the static site is meant to be served at `https://partle.rubenayla.xyz/documentation`.
- Preview locally:
  ```bash
  cd backend
  uv sync --extra docs          # installs mkdocs + theme
  uv run mkdocs serve -f ../mkdocs.yml
  ```
- Build static assets (deployable to any static host or the `/documentation` route):
  ```bash
  cd backend
  uv sync --extra docs
  uv run mkdocs build -f ../mkdocs.yml
  ```
- CI now runs `mkdocs build` on every push to ensure the docs compile before deployment.

---

## 🚀 Development Quick Start

### **Standard Port Configuration**

**Frontend (React + Vite):**
```bash
cd frontend
npm run dev -- --port 3000
```
→ **http://localhost:3000** (React/Vite standard)

**Backend (FastAPI + Python):**
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
→ **http://localhost:8000** (FastAPI standard)

### **Architecture Overview**
```
Frontend (3000) ──HTTP Requests──→ Backend (8000) ──→ PostgreSQL (Hetzner)
```

### Local URLs

* **Frontend:** [http://localhost:3000/](http://localhost:3000/) ⭐
* **Backend API:** [http://localhost:8000/](http://localhost:8000/)
  * [http://localhost:8000/docs](http://localhost:8000/docs)    (API docs)
  * [http://localhost:8000/redoc](http://localhost:8000/redoc)   (ReDoc docs)
  * [http://localhost:8000/v1/products/](http://localhost:8000/v1/products/)  (Products API)
  * [http://localhost:8000/v1/stores/](http://localhost:8000/v1/stores/) (Stores API)
  * [http://localhost:8000/v1/products/286/image](http://localhost:8000/v1/products/286/image) (Sample image)

### Frontend tips & troubleshooting
- Vite defaults to port `5173`. We pin to `3000` with `npm run dev -- --port 3000`, but if 3000 is busy Vite will auto-increment. Check which PID uses the port (`sudo lsof -i :3000`) and kill it (`kill -9 <PID>`) before restarting.
- Production build: `npm run build` generates `frontend/dist/` ready for any static host.
- `npm WARN Unknown env config "http-proxy"` usually comes from stale npm config. Clear it with `npm config delete http-proxy` / `npm config delete https-proxy`, or remove the setting from `~/.npmrc`.

## Email delivery (Cloudflare Worker → Resend)

MailChannels removed their free Cloudflare Worker tier on **2024-08-31**, so all outbound mail now uses [Resend](https://resend.com/).

### Setup flow
1. Create a Resend account (free tier: 100 emails/day, 3000/month).
2. Use the “Sign in with Cloudflare” integration so Resend adds DNS records automatically.
3. Add the Resend API key to the Worker (`RESEND_API_KEY` secret) and update `/stuff/cloudflare-email-worker.js` to call `https://api.resend.com/emails`.
4. Only send from verified addresses (e.g., `noreply@rubenayla.xyz`).

### Required DNS (added by the integration)
- MX: `send` → `feedback-smtp.eu-west-1.amazonses.com`
- DKIM: `resend._domainkey` → Resend-provided DKIM value
- SPF: `v=spf1 include:amazonses.com ~all`

### Migration notes
- Old MailChannels flow (`api.mailchannels.net` + `_mailchannels` TXT Domain Lockdown) no longer authenticates.
- Cloudflare Email Routing is receive-only; it cannot send mail.
- Resend silently drops mail until DNS verification propagates—double-check via their dashboard.

### References
- [Cloudflare Workers email docs](https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/)
- [MailChannels shutdown notes](https://support.mailchannels.com/hc/en-us/articles/16918954360845)
- [Resend + Cloudflare tutorial](https://resend.com/docs/send-with-cloudflare-workers)

### Key files
- `stuff/cloudflare-email-worker.js` – Worker script that calls Resend
- `backend/app/auth/utils.py` – Backend helpers that trigger emails
- `backend/test_email_debug.py` – Manual test harness

## Search engine (Elasticsearch)

Elasticsearch powers fuzzy matching, geo filters, and aggregations. The backend falls back to `/v1/products/` if the cluster is offline, but you get the best results when search is running.

### Local setup
```bash
# Start Elasticsearch container
docker compose up -d elasticsearch

# Initialize mappings + index + seed
cd backend
uv run python manage_search.py setup   # init + reindex + info
```

Additional helpers:
```bash
uv run python manage_search.py check       # ping cluster
uv run python manage_search.py init        # create index
uv run python manage_search.py init-force  # recreate index
uv run python manage_search.py reindex     # bulk index products
uv run python manage_search.py info        # show stats
```

### API surface
- `GET /v1/search/products/` – main endpoint (`q`, `min_price`, `max_price`, `tags`, `store_id`, `lat/lon/distance_km`, `sort_by`, `limit`, `offset`, `include_aggregations`).
- `GET /v1/products/` – legacy fallback when search is unavailable.
- `GET /v1/search/health` – health probe.

### Configuration
```
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=products
```

### Monitoring & troubleshooting
```bash
curl http://localhost:9200/products/_stats
curl http://localhost:9200                 # verify service
docker logs partle-elasticsearch
```
- “Elasticsearch not available” → ensure Docker container is running.
- “Index not found” → `uv run python manage_search.py init`.
- Empty results → `uv run python manage_search.py reindex`.
- Docker permission errors → add your user to the docker group (`sudo usermod -aG docker $USER`).

## DB Structure
tags
- id (PK)
- name (unique)

tag_links
- tag_id (FK)
- entity_type (Enum: 'product', 'store')
- entity_id (int)
- UNIQUE (tag_id, entity_type, entity_id)


## 📆 Project Structure

```bash
partle/
├── frontend/
│   ├── public/                         # Static assets (includes robots.txt, ai.txt, sitemap.xml, openapi.json)
│   └── src/
│       ├── assets/                    # Logos, icons, etc
│       ├── components/                # Reusable UI components
│       ├── pages/                     # Views (Home, Stores, Products, etc.)
│       │   └── ProductDetail.jsx      # Product detail page with Schema.org structured data
│       ├── data/                      # Temp: mock JSON data
│       ├── App.tsx                    # Main routing
│       ├── main.tsx                   # React root (HelmetProvider configured here)
│       └── index.css                  # Tailwind entrypoint
│   ├── index.html
│   ├── package.json                   # react-helmet-async dependency added here
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
│   ├── pyproject.toml                 # UV/Python project config
│   ├── uv.lock
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
