disable test products by default, somehow


# todo ruben check sku
  🎯 SKU Implementation Summary

  Backend Changes

  1. Database Model (app/db/models.py):
    - Added sku field (String(50), nullable, indexed)
    - Added composite unique constraint on (store_id, sku)
    - This ensures SKUs are unique per store but can be reused across stores
  2. Migration (alembic/versions/ffbebe72d891_add_sku_field_with_per_store_uniqueness.py):
    - Successfully migrated database with SKU field
    - Added index for faster SKU lookups
    - Created unique constraint unique_store_sku
  3. API Schema (app/schemas/product.py):
    - Added sku to ProductIn, ProductUpdate, and ProductOut schemas
    - SKU is optional but validated when provided
  4. Bulk Import (app/routes/bulk_import.py):
    - Added SKU column support
    - Validates SKU uniqueness during import
    - Returns clear error if duplicate SKU found

  Frontend Changes

  1. Type Definition (src/types/index.ts):
    - Added sku?: string to Product interface
  2. Display Utility (src/utils/product.ts):
    - getProductIdentifier() - Returns SKU or #ID
    - getProductIdentifierWithLabel() - Returns "SKU: XXX" or "ID: #XXX"
    - hasCustomSKU() - Checks if product has custom SKU
  3. Product Detail Page (src/pages/ProductDetail.tsx):
    - Shows SKU below product name (or #ID if no SKU)
    - Edit form includes SKU field with helpful description
    - SKU is saved when updating product
  4. Bulk Import UI (src/pages/BulkImport.tsx):
    - Supports SKU column in CSV/Excel files
    - Templates include SKU as first column

  Sample Templates

  - CSV and Excel templates now include SKU column
  - Example SKUs like "LAPTOP-001", "MOUSE-WL-02"
  - Instructions explain SKU is optional and unique per store

  Key Features

  ✅ Per-Store Uniqueness: Each store can have "PROD-001", no conflicts
  ✅ Optional Field: Works without SKU (displays #ID instead)
  ✅ Bulk Import Support: Can import products with SKUs
  ✅ User-Friendly: Clear labeling and helpful hints in UI
  ✅ Future-Proof: Can add franchise-wide SKUs later if needed

  This implementation gives stores professional inventory management capabilities while
  keeping it simple for those who don't need SKUs!



# todo ruben check bulk import:
I've successfully created a comprehensive bulk product import system for Partle! Here's
  what was implemented:

  ✅ Backend Features

  1. Bulk Import Endpoint (/v1/stores/{store_id}/bulk-import)
    - Accepts CSV or Excel files with product data
    - Supports ZIP files with product images
    - Validates data (name and price required)
    - Processes images and stores them in the database
    - Handles tags automatically
  2. Template Endpoints
    - /v1/import-template - Downloads sample CSV/Excel templates
    - /v1/import-instructions - Returns detailed import instructions
  3. Data Validation
    - Checks for required columns
    - Validates price data
    - Handles errors gracefully with detailed feedback

  ✅ Frontend Features

  1. Bulk Import Page (/stores/:storeId/bulk-import)
    - Drag-and-drop file upload for CSV/Excel
    - Optional ZIP upload for images
    - Download template buttons
    - Real-time import progress
    - Error reporting with specific row details
    - Success summary with statistics
  2. Store Card Enhancement
    - Added "Import" button for store owners
    - Shows only when the current user owns the store
    - Quick access to bulk import functionality

  ✅ Sample Templates Created

  - product_import_template.csv - Simple CSV format
  - product_import_template.xlsx - Excel with instructions sheet
  - minimal_import.csv - Quick testing template

  📋 How Store Owners Use It

  1. Navigate to their store page
  2. Click "Import" button (green upload icon)
  3. Download a template (CSV or Excel)
  4. Fill in product details
  5. Optionally prepare a ZIP with product images
  6. Upload both files
  7. View import results and any errors

  🔑 Key Features

  - Easy to use: Simple drag-and-drop interface
  - Flexible formats: Supports both CSV and Excel
  - Image support: Bulk upload product images via ZIP
  - Tag management: Automatically creates/assigns tags
  - Error handling: Clear feedback on what went wrong
  - Owner-only access: Only store owners can bulk import

  This system makes it incredibly easy for medium-small stores to quickly add their entire
   inventory to Partle!

---

test bulk add

- take location into account for sorting. Add Closest first option, and ask for location permission if not given yet
- i see a few new markdown files in the docs folder. Should we use mkdocs?
- Improve the scrapers so they get the image url and place it on the products in my website. I don't need to store the image, just the url. They would look much better.


We have lots of stores in the database, which have been scraped. Do we have their location? coordinates? If not, i think we should check the scraping software to check if the website where we got it from does have the info or not.

what happens if i enter a username that's already been used.

partle add true ratings, user product pair, link a number, note the time, aggregate them with ponderation based on date, somehow. Maybe not the date, but the 0rating order, so each previous rating is worth r times the later one, where r < 1


- How to modify product. If you are the user, when you click a product to see it, allow editing? Or do it in other way


---


# mcp for scraping when 5+ scrapers running
● Honest Assessment: MCP Scraping Agent

✅ PROS:
- Real examples exist - Firecrawl, Bright Data, crawl4ai MCP servers already working
- Autonomous monitoring - Can detect stuck scrapers, restart them, analyze logs
- Site adaptation - Could automatically adjust selectors when sites change
- Source discovery - Research and test new scraping targets
- Integration ready - Your Scrapy setup could plug into MCP easily

❌ CONS:
- Overkill for current scale - You have 2 spiders, not 50
- Development overhead - Weeks to build vs. minutes to fix spider limits
- Cost complexity - Need hosting, monitoring infrastructure
- New failure points - Agent could break scrapers that work fine
- Security risks - 2025 research shows MCP has prompt injection vulnerabilities

---

- in product page, a clear "Back" button that goes to the previous page
- In add product, add capability to add tags like #tag1 
- Add buttons to get feedback from users, and form page to receive it. The buttons will link to that page.
- Add several products fast and check they're there.
- Scrape products
- Create docs with sections for API use (people should be able to connect easily), database structure, standards, etc.
- [products|stores] toggle should go under filters
- MAKE MOBILE VERSION

- Store CRUD (3 → 4) – lets you seed real data from the UI.
- Parts under stores (5 → 6) – completes the core data model.
- Tune the reliability rating of the info uploaded. It should go -1 to 1. Start at 0, depending on other people ratings get modified.
- Users should be able to add products from other stores. Last updated time should be stored as parameter for every product. And who did that last update is relevant too.
- Get data
    - Scraping?
        - Google Maps
        - Amazon
        - Wallapop?
    - Ask gpt sources
- Mobile version (bar at the bottom with easy interface. Go ahead to new standards)
- The product of each store must have a unique name. If you don't agree with the data, several versions will appear, with capability to up/down vote them. It just like several products squished together in the same frontend card.
- seo for chatgpt searches so I can get pro users that will actually buy, being of benefit to the stores. Can charge the stores instead of the user, since use through chatgpt will be free

- once db is working with remote computer, not locally, tell codex to scrape sites, add the scraping software with tests and actually do some scraping
- Users report products (illegal etc)
- Improve unit tests
- Map toggle (7) – visual polish that sells the idea.
- add "Forgot password?" via email, need email service
    - configure .env for email service
- Hosting partle.rubenayla.xyz
- Add some color
- Ok, now i'd like to implement the feature to recover my password. The typical button "Forgot your password?" or "Recover your password with an email" something like that.

- use uptimerobot

## Not urgent, long term
- fix search box in chrome when scrolling
- When we got to the end of the page, Use Shopify Storefront API directly:
  - Public API, no authentication needed for product search
  - GraphQL for flexible queries
  - Pagination support for infinite scroll
  - Product data includes prices, images, descriptions
- AI search, call chatgpt with search engine to add better product results when doing searches that result in few or no products
- Mechanism to store searches performed by users so we can know what products are more demanded
- How to optimize for AI like chatgpt, so they can use my website to search or see the results from my website
    - Think super long term: My AI knows what i have and what i need, and automatically searches for the best products for me. Once one is good enough, it suggests it to me, taking even my calendar into account, when will i need it, time to arrive etc.
- limit max item count per row to 3?
- Think of better name. People don't understand what it is, how to write etc.
- Allow custom images and add the UI to add them, so we don't depend on other websites.
- Ask gemini to try to implement FIDO2. I think the best way is using SimpleWebAuthn. I already have Node.js for the frontend, so no extra dependencies. Should probably use the same PostgreSQL database i have, let Node return user_id and email, FastAPI issues the token.
- AI thingy to load them to the database just by recording with the phone. It recognizes the products, screenshots them, lists the price, geo location and everything. You can go around stores and record to add thousands of products.
- What if i put the search terms at the left, the search bar at the top of the left section, and on startup the website already includes products as suggestions? The left search terms stay there, and the scroll only includes the products. The right is blank or left for ads etc.
- Make map take the whole screen while keeping list with 4xl
Explore direct public key login (passkeys) so the browser handles authentication. If the key is lost, allow email-based reset.
- Do evaluation of each metric by the users, when
- Consider composite search mode with slide bars to select what I care more about, and instead of filter do a score assignation. For example, prioritize stock and distance over price when it's urgent, or prioritize price 
- Do AI search, consider external services or a language model that maps high level abstraction of the query with the closest product matches in the vector space.
- Implement multiple login methods:
    - Passkey (WebAuthn) for passwordless authentication.
    - Google-linked authentication (OAuth 2.0).
    - Ensure all methods link to a single user identity.
    - Provide options for managing these methods in account settings.
- Add 'relevant' sorting method
- Search with regex?
- Search with free form descriptions and use AI, creating abstractions of the product and the search, and mapping the closest?
    - Or just let chatgpt search using our api
- MCP should let my personal AI look around for products that will be actually interesting to me, and that AI, my personal one that might even run locally or with privacy taken into account, with my data safe, it will decide what i probably want, and suggest it to me, instead of letting external AIs spam me with ads. I believe the ad industry is going to change. We can achieve superhuman efficiency letting the AI even do purchases below a certain price threshold. If we happen to be close to a store that has what we want, just notify us and let us know we don't even have to search for it or travel. I there's something i don't want and has value, it might suggest me to sell it, with a client alreay ready to buy. Since the client is an AI, this is not wasting anyone's time. They could be like 'potential' transactions performed by the AI, and when both human parties agree, it's performed with ease.
- can we load empty boxes while loading the products, to make the ui look faster? Like Youtube or Wallapop do.