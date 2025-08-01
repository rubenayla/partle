
import json
import os
from app.main import app

# Set the environment to prevent errors if .env is not found
os.environ["RAILWAY_ENVIRONMENT"] = "production"

# Generate the OpenAPI schema
openapi_schema = app.openapi()

# Set the version and servers
openapi_schema["info"]["version"] = "v1"
openapi_schema["servers"] = [
    {"url": "https://partle.vercel.app/api"},
    {"url": "http://localhost:8000"},
]


# Write the schema to a file
with open("../frontend/public/api/openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("Successfully generated openapi.json")
