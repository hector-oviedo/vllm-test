import json
from .main import app

def generate_openapi():
    openapi_schema = app.openapi()
    with open("docs/openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("✅ Generated docs/openapi.json")

if __name__ == "__main__":
    generate_openapi()
