- UI
    - The text on hover showing shortcuts and whatnot should appear immediately, not after a delay. 


------

- Ok, now i'd like to implement the feature to recover my password. The typical button "Forgot your password?" or "Recover yourpassword with an email" something like that.   
- Add tags table according to README.md
    - Then, add mock data to the database with a corresponding tag. use api that mocks data? or let gpt fill it
- add recover password email, need vercel or something
- consider types of stores, and start adding them
- Store CRUD (3 → 4) – lets you seed real data from the UI.
- Parts under stores (5 → 6) – completes the core data model.
- Tune the reliability rating of the info uploaded. It should go -1 to 1. Start at 0, depending on other people ratings get modified.
- Users should be able to add products from other stores. Last updated time should be stored as parameter for every product. And who did that last update is relevant too.
- Add tags table, for products
    - like my favourites ones, just a tag for those, to play
- Get data
    - Scraping?
        - Google Maps
        - Amazon
        - Wallapop?
    - Ask gpt sources
- Make theme mode auto actually work based on the browser theme
- Mobile version (bar at the bottom with easy interface. Go ahead to new standards)
- The product of each store must have a unique name. If you don't agree with the data, several versions will appear, with capability to up/down vote them. It just like several products squished together in the same frontend card.
- Mechanism to store searches performed by users so we can know what products are more demanded
- seo for chatgpt searches so I can get pro users that will actually buy, being of benefit to the stores. Can charge the stores instead of the user, since use through chatgpt will be free
- Users report products (illegal etc)
- Improve unit tests
- Map toggle (7) – visual polish that sells the idea.
- Hosting partle.rubenayla.xyz

## Not urgent, long term
- Think of better name. People don't understand what it is, how to write etc.
- - Ask gemini to try to implement FIDO2. I think the best way is using SimpleWebAuthn. I already have Node.js for the frontend, so no extra dependencies. Should probably use the same PostgreSQL database i have, let Node return user_id and email, FastAPI issues the token.
- AI thingy to load them to the database just by recording with the phone. It recognizes the products, screenshots them, lists the price, geo location and everything. You can go around stores and record to add thousands of products.
- What if i put the search terms at the left, the search bar at the top of the left section, and on startup the website already includes products as suggestions? The left search terms stay there, and the scroll only includes the products. The right is blank or left for ads etc.
- Make map take the whole screen while keeping list with 4xl
Explore direct public key login (passkeys) so the browser handles authentication. If the key is lost, allow email-based reset.
- Do evaluation of each metric by the users, when
- Consider composite search mode with slide bars to select what I care more about, and instead of filter do a score assignation. For example, prioritize stock and distance over price when it's urgent, or prioritize price 
- Do AI search, consider external services or a language model that maps high level abstraction of the query with the closest product matches in the vector space.