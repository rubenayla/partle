# Possible names
Partora, Partle, PartNow, Localon, Locado,
- Discarded:
  - Partle: too hard to pronounce

MVP: Need search bar, map, and list of stores with their locations. Each product must have a name, price, associated store, qty in stock, reliability for each data such as price etc. Let the users adjust it. Optional: picture, description, ratings...

- Suggested start by gpt:
    - Backend with Python (FastAPI), PostgreSQL (open source and more powerful) but SQLite for MVP
    - Auth: None for now. Admin only.
    - Hosting: Railway.app or Fly.io for MVP. Why not cloudflare?
    - Frontend: React + Vite + Tailwind CSS + Leaflet
        > Requirement: Need to have a search option like AliExpress or Wallapop, + toggle that switches UI to map view, stores or products become dots over the map
        - React:     Component-based framework for building the dynamic UI (search, list, map toggle)
        - Vite:      Fast dev server and bundler for React; handles live reload and builds
        - Tailwind:  Utility-first CSS framework for rapid, clean styling without writing custom CSS
        - Leaflet:   Lightweight open-source map library to display stores as pins on a map

Data

## to add part (part post, try it out)
http://localhost:8000/docs#/Parts/add_part_v1_parts_post

{
  "name": "PH connector 6-pin",
  "sku": "JST-XH-6",
  "stock": 20,
  "price": 0.45,
  "store_id": 1
}


{
  "name": "4-Channel Logic Level Converter",
  "sku": "LLC-4CH",
  "stock": 10,
  "price": 1.80,
  "store_id": 1
}


{
  "name": "Soldering Iron 60W Adjustable",
  "sku": "SI-60W",
  "stock": 5,
  "price": 12.95,
  "store_id": 1
}

{
  "name": "Soldering Iron 60W Adjustable",
  "sku": "SI-60W",
  "stock": 5,
  "price": 12.95,
  "store_id": 1
}

# 2025-06-18
```
sudo apt install -y \
  build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncurses-dev libffi-dev liblzma-dev uuid-dev \
  libgdbm-dev tk-dev libnss3-dev libdb-dev libexpat1-dev \
  libxml2-dev libxmlsec1-dev libx11-dev libxext-dev libxrender-dev \
  xz-utils

pyenv uninstall 3.12.3  # if you haven't already
pyenv install 3.12.3
pyenv global 3.12.3

cd ~/repos/partle/backend
rm -rf .venv
poetry config virtualenvs.in-project true
poetry env use $(pyenv which python)
poetry install
poetry shell
```

# 2025-06-19
http://localhost:8000/ 
http://localhost:8000/docs
http://localhost:8000/v1/parts

# Poetry reminder
To enable venv: poetry shell
To run with venv but then come back: poetry run ...

# to login with terminal
```bash
LOGIN_RESPONSE=$(
  curl -s -X POST http://localhost:8000/auth/login \
    -F "username=ruben.jimenezmejias@gmail.com" \
    -F "password=partle"
)
TOKEN=$(echo $LOGIN_RESPONSE | jq -r .access_token)
echo "$TOKEN"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzUwMzU4NTMwfQ.ASnHKm2AQda8nZYc4Ct5GRt5VYBkiw_EqGi0VeXiU6g
curl -X POST http://localhost:8000/v1/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"JST-PH 2-pin","price":"0.12","store_id":1}'
{"store_id":1,"name":"JST-PH 2-pin","spec":null,"price":"0.12","url":null,"lat":null,"lon":null,"description":null,"id":1}curl http://localhost:8000/v1/products/?store_id=1                 curl http://localhost:8000/v1/products/?store_id=1
[{"store_id":1,"name":"JST-PH 2-pin","spec":null,"price":"0.12","url":null,"lat":null,"lon":null,"description":null,"id":1}]
```

# websites for ui inspiration
- https://www.airbnb.com/
- https://dribbble.com/search/ui
- https://www.olx.com.br/
- https://www.etsy.com/
- https://www.zillow.com/
- https://open.spotify.com/

# 2025-06-20
![](stuff/20250620003901.png)

![](stuff/20250620005012.png)

![](stuff/20250620010811.png)

Version with white bar and shaded background.
I prefer flat colors, white background and grey search bar, I think.
![](stuff/20250620015440.png)

What options do i want in Account button?
- If the user is not logged in, these options can't be performed, so just show the Account page. Otherwise:
  - Premium accounts and stuff like that, in the future
  - Light/Dark/Auto theme linked to account
  - Favourite stores
  - Favourite products (Maybe custom lists in the future)
  - Log out

Oh and I also want a 'i' of info icon with the Contact page and stuff like that.

![](stuff/20250620031426.png)

![](stuff/20250620112149.png)


# backend self check
```bash
poetry run python - <<'PY'
from app.main import app
print("\n".join(f"{r.path}  {sorted(r.methods)}" for r in app.routes))
PY
```

```bash
curl -X POST http://localhost:8000/v1/auth/fido/register/begin \
     -H "Content-Type: application/json" \
     -d '{"email":"ruben.jimenezmejias@gmail.com"}'
```

# i'm having problems with this
```bash
(.venv) rubenayla@y5curl -XPOST http://127.0.0.1:8000/v1/auth/register \0.1:8000/v1/auth/register \
     -H 'Content-Type: application/json' \
     -d '{"email":"test@example.com","password":"dummy"}'
{"status":"ok"}(.venv) rubenayla@y540:~/repos/pcurl -XPOST http://127.0.0.1:8000/v1/auth/fido/register/begin \egister/begin \
     -H 'Content-Type: application/json' \
     -d '{"email":"test@example.com"}'   # should now return 200 with challenge JSON
Internal Server Error(.venv) rubenayla@y540:~/repos/partle/backend$ 
```

# 2025-06-21 I give up on fido2 for now. Leave this here as notes
```python
# backend/app/api/v1/auth.py
"""
Things we learned trying to make this work:
- Accessing `Credential.id` directly is fine for constructing login descriptors, *but* you must also supply `type=PublicKeyCredentialType.PUBLIC_KEY` when you build a `PublicKeyCredentialDescriptor`.
- `AttestedCredentialData` is the right type for credentials passed to `authenticate_complete()`, not `PublicKeyCredentialDescriptor`.
- `AuthenticatorData` (our `auth_data` var) does **not** expose `sign_count`; use `auth_data.counter`.
- `AuthenticatorData` parses from raw bytes and gives structured fields (`rp_id_hash`, `flags`, `credential_data`, ...).
- `CollectedClientData` must be built from base‑64‑decoded bytes, not raw JSON.
- `CredentialRequestOptions` / `PublicKeyCredentialCreationOptions` returned by the FIDO2 server are mapping‑like objects; they don’t implement `.to_dict()` and they contain raw `bytes`.
- They support *attribute* access (`.challenge`) but not `obj["challenge"]`, and they are immutable.
- Mixing blog posts from different fido2 versions leads to bad assumptions.
- `PublicKeyCredentialUserEntity` must be an object, not a plain dict.
- FastAPI generator deps must be annotated `Generator[Session, None, None]` or the linter yells.
- Use `Any` from `typing`, not builtin `any`.
- `UserVerificationRequirement.PREFERRED` (enum) is required, not the string "preferred".
- Every field that reaches the browser (`challenge`, `user.id`, `allowCredentials[*].id`, ...) must be *base64url strings*; leave them as raw bytes only when talking to the fido2 library.
- `exclude_credentials` can be `None`; loop safely.
- `asdict()` converts dataclasses to **snake_case** keys (`public_key`), so we converted them to **camelCase** for WebAuthn.
- Converting dataclasses to camelCase requires renaming keys, *not* renaming variables; keep `user` in scope.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Generator, cast

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.auth.utils import (
    create_access_token,
    create_reset_token,
    hash_password,
    send_reset_email,
    verify_password,
)
from app.db.models import Credential, User
from app.db.session import SessionLocal
from app.schemas import auth as schema

from fido2.server import Fido2Server
from fido2.utils import websafe_decode, websafe_encode
from fido2.webauthn import (
    AttestationObject,
    AuthenticatorAssertionResponse,
    AuthenticatorData,
    CollectedClientData,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialType,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
    UserVerificationRequirement,
)

router = APIRouter()

rp = PublicKeyCredentialRpEntity(id="localhost", name="Partle")
fido_server = Fido2Server(rp)

register_states: Dict[str, Any] = {}
auth_states: Dict[str, Any] = {}


# ───────── helper utils ─────────


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def snake_to_camel(key: str) -> str:
    head, *tail = key.split("_")
    return head + "".join(word.title() for word in tail)


def camelify(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {snake_to_camel(k): camelify(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [camelify(v) for v in obj]
    return obj


def b64ify(obj: Any) -> Any:
    if isinstance(obj, (bytes, bytearray)):
        return websafe_encode(obj)
    if isinstance(obj, dict):
        return {k: b64ify(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [b64ify(v) for v in obj]
    return obj


# ───────── password auth ─────────


@router.post("/register")
def register(data: schema.RegisterInput, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(409, "User already exists")
    db.add(User(email=data.email, password_hash=hash_password(data.password)))
    db.commit()
    return {"status": "ok"}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form.username).first()
    if (
        not user
        or not user.password_hash
        or not verify_password(form.password, user.password_hash)
    ):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_access_token({"sub": str(user.id)})}


@router.post("/request-password-reset", status_code=202)
def request_password_reset(
    payload: schema.EmailOnly,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=payload.email).first()
    if user:
        background_tasks.add_task(
            send_reset_email, user.email, create_reset_token(user)
        )
    return {"status": "ok"}


@router.get("/me", response_model=schema.UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# ───────── FIDO2 register ─────────


@router.post("/fido/register/begin")
def fido_register_begin(payload: schema.EmailOnly, db: Session = Depends(get_db)):
    # ensure user exists (password_hash may stay None)
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        user = User(email=payload.email, password_hash=None)
        db.add(user)
        db.commit()
        db.refresh(user)

    user_entity = PublicKeyCredentialUserEntity(
        id=str(user.id).encode(),
        name=user.email,
        display_name=user.email,
    )

    options_obj, state = fido_server.register_begin(
        user=user_entity,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    # build browser payload
    options_dict = asdict(options_obj)
    options_camel = camelify(options_dict)
    options_b64 = b64ify(options_camel)

    register_states[user.email] = state
    return jsonable_encoder({"publicKey": options_b64})


@router.post("/fido/register/finish")
def fido_register_finish(
    payload: schema.FidoRegisterFinish, db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    state = register_states.pop(user.email, None)
    if not state:
        raise HTTPException(400, "No registration in progress")

    response = RegistrationResponse.from_dict(payload.credential)
    auth_data = fido_server.register_complete(state, response)

    if auth_data.credential_data is None:
        raise HTTPException(400, "No attested credential data returned")

    db.add(
        Credential(
            credential_id=auth_data.credential_data.credential_id,
            public_key=auth_data.credential_data.public_key,
            sign_count=auth_data.counter,
            user_id=user.id,
        )
    )
    db.commit()

    return {"access_token": create_access_token({"sub": str(user.id)})}
```

# 2025-06-21
First uses of Vercel

![](stuff/20250621203343.png)

# 2025-06-21--22-23
Using Vercel for frontend and Railway for backend. I'm on Railway free plan.


Thinking about Pieter Levels setup, he'd probably move backend to GCE (Google Compute Engine) VM, gpt says i'd need either docker-compose or tmux to keep FastAPI + PostgreSQL running. Big big apps use Kubernetes but he doesn't use it. Stick to simple.

Serve frontend with GCS (Google Cloud Storage) bucket or cloudflare pages.

For the data, Postgres on the same VM as backend + daily pg_dump to the GCS bucket.

Github Actions cool to run script on push code, like run tests and deploy backend to GCE via ssh.


## ✅ Auth & Deployment Fixes (Jun 21–22)

- 🔐 Switched AuthModal to **password-only** login (removed FIDO/passkey logic)
- 🌐 Replaced dead `fly.dev` backend URL with Railway deployment:
  - `VITE_API_BASE = https://partle-production.up.railway.app`
- 🛡️ Fixed **CORS policy**:
  - Added `https://partle.vercel.app` to `allow_origins` in backend `main.py`
- 🛠️ Resolved TypeScript error (`import.meta.env`) by adding `vite-env.d.ts`
- 🚀 Redeployed frontend (Vercel) and backend (Railway) to apply fixes

##
```bash
(.venv) rubenayla@y540:~/repos/partle/backend$ sudo -u postgres psql
psql (16.9 (Ubuntu 16.9-0ubuntu0.24.04.1))
Type "help" for help.

postgres=# \l
                                                       List of databases
   Name    |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | ICU Rules |   Access privileges   
-----------+----------+----------+-----------------+-------------+-------------+------------+-----------+-----------------------
 partle    | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 postgres  | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 template0 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
(4 rows)

postgres=# \c partle
You are now connected to database "partle" as user "postgres".
partle=# \dt
              List of relations
 Schema |      Name       | Type  |  Owner   
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | credentials     | table | postgres
 public | products        | table | postgres
 public | stores          | table | postgres
 public | users           | table | postgres
(5 rows)

partle=# SELECT * FROM users;
 id |             email             |                        password_hash                         
----+-------------------------------+--------------------------------------------------------------
  1 | demo@partle.dev               | $2b$12$jyztUAFohj8XD80DbjAhTerTlXm5lUs4b14RRJC9BB/YP6F06lGY.
  2 | caca@gmail.com                | $2b$12$xd4ZNPpi9MD0llPKg8fyGe/O0sT8PfpDBhR.CAIr2rssJhl6KHlo6
  4 | test@gmail.com                | $2b$12$/Qlxv5PG7LHGlcUNqJ3tRO16eZWiYs6iW6y7fSTo4xb72dYSLUd2y
  3 | ruben.jimenezmejias@gmail.com | $2b$12$76W5x5gGrpoouN49Yd3b4.TEINDXSLw3ArXoGMGoUJNYFwUL416Cm
  5 | pato@gmail.com                | $2b$12$2UEdjAwZtziJ.uoM//5J2etuBUcAy54Ex2Xn26AVWXAn9MB2LkhSO
  6 | patopato@gmail.com            | 
  7 | patoo@gmail.com               | 
  8 | test@example.com              | $2b$12$f2hzfDYbtn9frK6KywelcOTNIp9YwXo4jU0rYvHwENL391Ufy/KFG
  9 | a@gmail.com                   | 
 10 | b@gmail.com                   | $2b$12$VHjYY7l2nxIcMuXMQ5nD6.FfCnkUQoAbLBATXlIjZlCDMTWHTh0Pm
(10 rows)

partle=# 
```
## shitty railway errors
![](stuff/20250622015320.png)


learned my lesson. Use a GCE directly.
e2-micro VM should be cheap.
BUT, remember, i have a laptop 24/7, I'm gonna use that.

# 2025-07-27
For now i'll use my laptop as the backend server, the page will go down everytime i turn it off since i'm still in development

# format and scraping
## Leroy Merlin
uses productos in the link so it's easy to distinguish. Maybe the spider crawler and that's it
https://www.leroymerlin.es/productos/perfil-forma-cuadrada-de-acero-en-bruto-standers-alt-25-x-an-25mm-x-l-1-m-87825775.html
BLOCKED, BOT DETECTION. HARD

## bricodepot
https://www.bricodepot.es/carpa-plegable-verde-2-6-x-3-x-3-m-8421415191695

https://www.elcorteingles.es/electrodomesticos/A42712840-lavadora-haier-8-kg-1400-rpm-vapor-i-pro-series-3-hw80-b14939-ib/?stype=search_redirect&parentCategoryId=999.54508013&color=Blanco

# 2025-07-27 Installation issues from codex
Backend issues

Running migrations without DATABASE_URL aborts immediately with ⛔ DATABASE_URL not set; aborting migrations.

Using SQLite (DATABASE_URL=sqlite:///partle.db) fails because Alembic attempts ALTER TABLE … DROP NOT NULL, which SQLite does not support, causing sqlite3.OperationalError: near "ALTER": syntax error

After installing and starting PostgreSQL, migrations succeed and the server starts correctly (Uvicorn log shows startup)

Running backend tests via poetry run pytest results in one failure: tests/test_auth_utils.py::test_send_reset_email raises SMTPServerDisconnected: please run connect() first because the test tries to send an email without a configured SMTP server

Frontend issues

npm install completes but shows npm WARN Unknown env config "http-proxy".

Starting the dev server shows port conflicts and the same Unknown env config warning before falling back to port 5175

Running npm test passes, but jsdom logs network errors because Axios tries to fetch /api/v1/products while the backend is unreachable during tests

Testing

Backend tests: poetry run pytest -q → 1 failed, 22 passed

Frontend tests: npm test → tests pass but output shows cancellation after network errors

# 
✦ I have updated the StoreScrapersItem and created a new Scrapy spider named ferreterias.py.

  To run this spider, you would navigate to the backend/app/scraper/store_scrapers/ directory in your terminal and execute the following command:

   1 scrapy crawl ferreterias -o ferreterias_output.json

# to add ferreterias
OpenStreetMap

# 2025-07-29  
● The Problem Explained in Detail

  The search functionality failure was caused by a timing/lifecycle bug in how React components communicate. Here's exactly what was happening:

  🔥 The Core Issue: Component Communication Timing

  The Problem:
  // In Layout.tsx - BROKEN
  onSearch={isHomePage ? (window as any).homeSearchHandler : undefined}

  1. Layout component renders first when the app loads
  2. At this moment, window.homeSearchHandler is undefined (Home component hasn't mounted yet)
  3. Layout passes undefined to SearchBar as the onSearch prop
  4. SearchBar defaults undefined to an empty function: onSearch = () => { }
  5. Home component mounts later and sets window.homeSearchHandler
  6. But SearchBar still has the original empty function - the connection is broken

  🔧 The Fix: Dynamic Handler Resolution

  The Solution:
  // In Layout.tsx - FIXED
  onSearch={isHomePage ? (params: any) => {
    if ((window as any).homeSearchHandler) {
      (window as any).homeSearchHandler(params);
    }
  } : undefined}

  Instead of passing the handler directly, we pass a wrapper function that checks for the handler's existence at runtime, not at render time.

  🔍 Additional Issues Found & Fixed

  1. Wrong API Configuration
    - Problem: Home.jsx used raw axios instead of configured api instance
    - Result: No base URL, no auth headers, wrong endpoints
    - Fix: import api from "../api" and use /v1/products/ endpoints
  2. Circular Dependency in useCallback
    - Problem: fetchData had [searchParams, offset] dependencies
    - Result: Infinite re-creation loop preventing API calls
    - Fix: Empty dependency array [] and explicit parameter passing
  3. Test Infrastructure Missing
    - Problem: No comprehensive test coverage
    - Fix: Added @testing-library/user-event and full test suites
  4. Accessibility Issues
    - Problem: Buttons without accessible names
    - Fix: Added aria-label attributes

  🎯 Why This Was So Hard to Debug

  1. Multiple moving parts: Search UI → SearchBar → Layout → Home → API
  2. Timing dependency: The bug only occurred due to React component mount order
  3. Silent failure: No errors thrown, just empty functions being called
  4. State appeared correct: Console showed right parameters, but they never reached the API
  5. Multiple similar issues: API config problems masked the main timing bug



