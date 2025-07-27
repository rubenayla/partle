
how many stores?
- consider types of stores, and start adding them
- Start adding products
- MAKE MOBILE VERSION
- Simple api to use.
    - 1. see products. No auth required.
    - 2. auth and upload products
[products|stores] toggle should go under filters

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
- Users report products (illegal etc)
- Improve unit tests
- Map toggle (7) – visual polish that sells the idea.
- add "Forgot password?" via email, need vercel or something
    - vercel put .env as in the example?
- Hosting partle.rubenayla.xyz
- Add some color
- Ok, now i'd like to implement the feature to recover my password. The typical button "Forgot your password?" or "Recover your password with an email" something like that.


## Not urgent, long term
- Mechanism to store searches performed by users so we can know what products are more demanded
- How to optimize for AI like chatgpt, so they can use my website to search or see the results from my website
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