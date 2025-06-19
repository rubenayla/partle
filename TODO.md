- Demo user and part
    - http://localhost:8000/docs

- Hosting partle.rubenayla.xyz
- Backend
- Add Accounts
    > Required mainly just to upload products. Also rate them, save favourites, skip ads with paid tiers etc.
    - Default sign-in uses passkeys (WebAuthn/FIDO2)
    - Fallback to email + password
    - Single email field: existing emails sign in, new ones create an account
- add modification date to db and system
- Add API so clients can add products (and stores?)
- Add UI to add stores
- Add UI to add products
- Think of better name. People don't understand what it is, how to write etc.
- Tune the reliability rating of the info uploaded. It should go -1 to 1. Start at 0, depending on other people ratings get modified.
- Get data
    - Scraping?
        - Google Maps
        - Amazon
        - Wallapop?
    - Ask gpt sources
- The product of each store must have a unique name. If you don't agree with the data, several versions will appear, with capability to up/down vote them. It just like several products squished together in the same frontend card.
- Mechanism to store searches performed by users so we can know what products are more demanded
- Consider removing Tailwind CSS. What's it for?
- seo for chatgpt searches so I can get pro users that will actually buy, being of benefit to the stores. Can charge the stores instead of the user, since use through chatgpt will be free
- Users report products (illegal etc)

## Not urgent, long term
- AI thingy to load them to the database just by recording with the phone. It recognizes the products, screenshots them, lists the price, geo location and everything. You can go around stores and record to add thousands of products.
- What if i put the search terms at the left, the search bar at the top of the left section, and on startup the website already includes products as suggestions? The left search terms stay there, and the scroll only includes the products. The right is blank or left for ads etc.
- Mobile version (bottom to top, bar at the bottom with easy interface. Go ahead to new standards)
- Make map take the whole screen while keeping list with 4xl
Explore direct public key login (passkeys) so the browser handles authentication. If the key is lost, allow email-based reset.
- Do evaluation of each metric by the users, when
- Consider composite search mode with slide bars to select what I care more about, and instead of filter do a score assignation. For example, prioritize stock and distance over price when it's urgent, or prioritize price 
- Do AI search, consider external services or a language model that maps high level abstraction of the query with the closest product matches in the vector space.