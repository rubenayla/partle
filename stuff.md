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
- https://www.olx.com.br/
- https://www.etsy.com/
- https://www.zillow.com/

# 2025-06-20
![](stuff/20250620003901.png)

