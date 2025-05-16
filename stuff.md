Possible names: Partle, PartNow, Localon

MVP: Need search bar, map, and list of stores with their locations. Each product must have a name, price, associated store, qty in stock, reliability for each data such as price etc. Let the users adjust it. Optional: picture, description, ratings...

- Suggested start by gpt:
    - Backend with Python (FastAPI), PostgreSQL (open source and more powerful)
    - Auth: None for now. Admin only.
    - Hosting: Railway.app or Fly.io for MVP. Why not cloudflare?
    - Frontend: React + Vite + Tailwind CSS + Leaflet
        > Requirement: Need to have a search option like AliExpress or Wallapop, + toggle that switches UI to map view, stores or products become dots over the map
        - React:     Component-based framework for building the dynamic UI (search, list, map toggle)
        - Vite:      Fast dev server and bundler for React; handles live reload and builds
        - Tailwind:  Utility-first CSS framework for rapid, clean styling without writing custom CSS
        - Leaflet:   Lightweight open-source map library to display stores as pins on a map

Data